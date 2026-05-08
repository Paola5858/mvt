"""Testes unitários dos services: SyncService e processar_csv_medicoes."""
import io
import csv as csv_module
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from rest_framework.test import APITestCase

from api_telemetria.models import (
    Marca,
    Modelo,
    Veiculo,
    UnidadeMedida,
    Medicao,
    MedicaoVeiculoIoT,
)
from api_telemetria.services import SyncService, processar_csv_medicoes


# ---------------------------------------------------------------------------
# SyncService
# ---------------------------------------------------------------------------

class SyncServiceTestCase(APITestCase):
    def setUp(self):
        self.marca = Marca.objects.create(nome="MASSEY")
        self.modelo = Modelo.objects.create(nome="MF2715")
        self.veiculo = Veiculo.objects.create(
            descricao="Trator",
            marca=self.marca,
            modelo=self.modelo,
            ano=2020,
            horimetro=5000.0,
        )

    def _medicao(self, ts=None, **kwargs):
        return {
            "temperatura": 85.5,
            "vibracao": 2.3,
            "rpm": 2500,
            "timestamp_coleta": ts or datetime(2026, 4, 16, 10, 30, 0),
            **kwargs,
        }

    def test_sucesso_insere_registros(self):
        resultado = SyncService.processar_sync_offline(
            veiculo_id=self.veiculo.id,  # type: ignore
            medicoes_data=[self._medicao()],
        )
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["registros_inseridos"], 1)

    def test_lista_vazia_retorna_ignorado(self):
        resultado = SyncService.processar_sync_offline(
            veiculo_id=self.veiculo.id,  # type: ignore
            medicoes_data=[],
        )
        self.assertEqual(resultado["status"], "ignorado")
        self.assertEqual(resultado["registros_inseridos"], 0)

    def test_veiculo_inexistente_retorna_erro(self):
        resultado = SyncService.processar_sync_offline(
            veiculo_id=99999,
            medicoes_data=[self._medicao()],
        )
        self.assertEqual(resultado["status"], "erro")
        self.assertEqual(resultado["código_erro"], "VEICULO_NAO_EXISTE")

    def test_race_condition_veiculo_deletado(self):
        veiculo_id = self.veiculo.id  # type: ignore
        self.veiculo.delete()
        resultado = SyncService.processar_sync_offline(
            veiculo_id=veiculo_id,
            medicoes_data=[self._medicao()],
        )
        self.assertEqual(resultado["status"], "erro")
        self.assertEqual(resultado["código_erro"], "VEICULO_NAO_EXISTE")

    def test_bulk_create_1500_registros(self):
        base = datetime(2026, 4, 16, 10, 0, 0)
        medicoes = [
            self._medicao(
                ts=base + timedelta(seconds=i),
                temperatura=80 + (i % 20),
                vibracao=1 + (i % 5),
                rpm=2000 + (i % 1000),
            )
            for i in range(1500)
        ]
        resultado = SyncService.processar_sync_offline(
            veiculo_id=self.veiculo.id,  # type: ignore
            medicoes_data=medicoes,
        )
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["registros_inseridos"], 1500)
        self.assertEqual(
            MedicaoVeiculoIoT.objects.filter(veiculo=self.veiculo).count(), 1500
        )

    def test_duplicata_ignorada_por_ignore_conflicts(self):
        medicao = self._medicao()
        SyncService.processar_sync_offline(veiculo_id=self.veiculo.id, medicoes_data=[medicao])  # type: ignore
        resultado = SyncService.processar_sync_offline(veiculo_id=self.veiculo.id, medicoes_data=[medicao])  # type: ignore
        self.assertEqual(resultado["status"], "sucesso")
        self.assertIn(resultado["registros_inseridos"], [0, 1])
        self.assertEqual(MedicaoVeiculoIoT.objects.filter(veiculo=self.veiculo).count(), 1)


# ---------------------------------------------------------------------------
# processar_csv_medicoes (mockando FileSystemStorage e procedure)
# ---------------------------------------------------------------------------

def _build_csv(rows: list[dict]) -> MagicMock:
    """Monta um InMemoryUploadedFile fake com conteúdo CSV."""
    buf = io.StringIO()
    writer = csv_module.DictWriter(buf, fieldnames=["veiculoid", "medicaoid", "data", "valor"], delimiter=";")
    writer.writeheader()
    writer.writerows(rows)
    buf.seek(0)

    mock_file = MagicMock()
    mock_file.name = "test.csv"
    mock_file.__iter__ = lambda self: iter(buf)
    return buf, mock_file


class CSVImportServiceTestCase(APITestCase):
    def setUp(self):
        self.marca = Marca.objects.create(nome="FIAT")
        self.modelo = Modelo.objects.create(nome="UNO")
        self.veiculo = Veiculo.objects.create(
            descricao="Carro CSV",
            marca=self.marca,
            modelo=self.modelo,
            ano=2022,
            horimetro=1000.0,
        )
        self.unidade = UnidadeMedida.objects.create(nome="Horas")
        self.medicao = Medicao.objects.create(tipo="horimetro", unidade_medida=self.unidade)

    def _csv_content(self, rows):
        buf = io.StringIO()
        writer = csv_module.DictWriter(buf, fieldnames=["veiculoid", "medicaoid", "data", "valor"], delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
        buf.seek(0)
        return buf.read().encode("utf-8")

    @patch("api_telemetria.services.executar_procedure_pos_importacao")
    @patch("api_telemetria.services.FileSystemStorage")
    def test_csv_valido_insere_registros(self, mock_fs_cls, mock_proc):
        rows = [{"veiculoid": self.veiculo.id, "medicaoid": self.medicao.id, "data": "2024-01-15 00:00:00", "valor": "100.0"}]  # type: ignore
        content = self._csv_content(rows)

        # Simula o arquivo salvo sendo lido de volta
        mock_fs = MagicMock()
        mock_fs_cls.return_value = mock_fs
        mock_fs.save.return_value = "uuid_test.csv"

        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        with patch("api_telemetria.services.os.path.join", return_value=tmp_path):
            with patch("api_telemetria.services.os.makedirs"):
                arquivo_mock = MagicMock()
                arquivo_mock.name = "test.csv"
                resultado = processar_csv_medicoes(arquivo_mock)

        os.unlink(tmp_path)

        self.assertIn("arquivoid", resultado)
        self.assertEqual(resultado["total_linhas_arquivo"], 1)

    @patch("api_telemetria.services.executar_procedure_pos_importacao")
    @patch("api_telemetria.services.FileSystemStorage")
    def test_csv_cabecalho_invalido_levanta_erro(self, mock_fs_cls, _mock_proc):
        content = b"campo_errado;outro\n1;2\n"

        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        mock_fs = MagicMock()
        mock_fs_cls.return_value = mock_fs
        mock_fs.save.return_value = "uuid_bad.csv"

        with patch("api_telemetria.services.os.path.join", return_value=tmp_path):
            with patch("api_telemetria.services.os.makedirs"):
                arquivo_mock = MagicMock()
                arquivo_mock.name = "bad.csv"
                with self.assertRaises(ValueError):
                    processar_csv_medicoes(arquivo_mock)

        os.unlink(tmp_path)
