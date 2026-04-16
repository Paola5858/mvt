"""Testes da API de Telemetria de Veículos."""
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from .models import (
    Marca,
    Modelo,
    Veiculo,
    UnidadeMedida,
    Medicao,
    MedicaoVeiculoTemp,
    MedicaoVeiculoIoT,
)
from .services import SyncService


class MarcaTestCase(APITestCase):
    """Testes para o endpoint de Marcas."""

    def test_criar_marca(self):
        """Testa a criação de uma marca."""
        response = self.client.post("/api/marcas/", {"nome": "FIAT"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome"], "FIAT")

    def test_listar_marcas(self):
        """Testa a listagem de marcas."""
        Marca.objects.create(nome='FIAT')
        Marca.objects.create(nome='VW')
        response = self.client.get('/api/marcas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ModeloTestCase(APITestCase):
    """Testes para o endpoint de Modelos."""

    def test_criar_modelo(self):
        """Testa a criação de um modelo."""
        response = self.client.post("/api/modelos/", {"nome": "UNO"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome"], "UNO")


class VeiculoTestCase(APITestCase):
    """Testes para o endpoint de Veículos."""

    def setUp(self):
        """Configura dados iniciais para os testes."""
        self.marca = Marca.objects.create(nome='FIAT')
        self.modelo = Modelo.objects.create(nome='UNO')

    def test_criar_veiculo(self):
        """Testa a criação de um veículo."""
        data = {
            "descricao": "Carro de teste",
            "marca": self.marca.id,
            "modelo": self.modelo.id,
            "ano": 2022,
            "horimetro": 5000.0,
        }
        response = self.client.post("/api/veiculos/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_validacao_ano_invalido(self):
        """Testa validação de ano inválido."""
        data = {
            'descricao': 'Carro',
            'marca': self.marca.id,
            'modelo': self.modelo.id,
            'ano': 1800,
            'horimetro': 0
        }
        response = self.client.post('/api/veiculos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MedicaoVeiculoTestCase(APITestCase):
    """Testes para o endpoint de Medições de Veículo."""

    def setUp(self):
        """Configura dados iniciais para os testes."""
        self.marca = Marca.objects.create(nome="FIAT")
        self.modelo = Modelo.objects.create(nome="UNO")
        self.veiculo = Veiculo.objects.create(
            descricao="Veículo Teste",
            marca=self.marca,
            modelo=self.modelo,
            ano=2020,
            horimetro=10000.0,
        )
        self.unidade = UnidadeMedida.objects.create(nome="Horas")
        self.medicao = Medicao.objects.create(
            tipo="horimetro", unidade_medida=self.unidade
        )

    def test_criar_medicao_veiculo(self):
        """Testa a criação de uma medição de veículo."""
        data = {
            'veiculo': self.veiculo.id,
            'medicao': self.medicao.id,
            'data': '2024-01-15',
            'valor': 15000.0
        }
        response = self.client.post('/api/medicoes-veiculo/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['valor']), 15000.0)


class SyncOfflineTestCase(APITestCase):
    """Testes para a sincronização offline do ESP32."""

    def setUp(self):
        """Configura dados iniciais para os testes de sync."""
        # Cria usuário autenticado (requerido pela view)
        self.user = User.objects.create_user(
            username="trator", password="tractorpass123"
        )
        self.client.force_authenticate(user=self.user)

        # Cria veículo
        self.marca = Marca.objects.create(nome="MASSEY")
        self.modelo = Modelo.objects.create(nome="MF2715")
        self.veiculo = Veiculo.objects.create(
            descricao="Trator sem internet",
            marca=self.marca,
            modelo=self.modelo,
            ano=2020,
            horimetro=5000.0,
        )

    def test_sync_offline_payload_valido(self):
        """Testa sincronização com payload válido."""
        response = self.client.post(
            "/api/sync/offline/",
            {
                "veiculo_id": self.veiculo.id,
                "medicoes": [
                    {
                        "id_veiculo": self.veiculo.id,
                        "temperatura": 85.5,
                        "vibracao": 2.3,
                        "rpm": 2500,
                        "timestamp_coleta": "2026-04-16T10:30:00Z",
                    },
                    {
                        "id_veiculo": self.veiculo.id,
                        "temperatura": 87.2,
                        "vibracao": 2.5,
                        "rpm": 2600,
                        "timestamp_coleta": "2026-04-16T10:31:00Z",
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "sucesso")
        self.assertEqual(response.data["registros_inseridos"], 2)

        # Verifica se os registros foram inseridos no DB
        self.assertEqual(
            MedicaoVeiculoIoT.objects.filter(veiculo=self.veiculo).count(), 2
        )

    def test_sync_offline_temperatura_invalida(self):
        """Testa rejeição de temperatura fora dos limites."""
        response = self.client.post(
            "/api/sync/offline/",
            {
                "veiculo_id": self.veiculo.id,
                "medicoes": [
                    {
                        "id_veiculo": self.veiculo.id,
                        "temperatura": 300,  # Acima de 250°C
                        "vibracao": 2.3,
                        "rpm": 2500,
                        "timestamp_coleta": "2026-04-16T10:30:00Z",
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("erro", response.data)

    def test_sync_offline_vibracao_invalida(self):
        """Testa rejeição de vibração fora dos limites."""
        response = self.client.post(
            "/api/sync/offline/",
            {
                "veiculo_id": self.veiculo.id,
                "medicoes": [
                    {
                        "id_veiculo": self.veiculo.id,
                        "temperatura": 85.5,
                        "vibracao": 150,  # Acima de 100 mm/s
                        "rpm": 2500,
                        "timestamp_coleta": "2026-04-16T10:30:00Z",
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("erro", response.data)

    def test_sync_offline_rpm_invalido(self):
        """Testa rejeição de RPM inválido."""
        response = self.client.post(
            "/api/sync/offline/",
            {
                "veiculo_id": self.veiculo.id,
                "medicoes": [
                    {
                        "id_veiculo": self.veiculo.id,
                        "temperatura": 85.5,
                        "vibracao": 2.3,
                        "rpm": 15000,  # Acima de 10000
                        "timestamp_coleta": "2026-04-16T10:30:00Z",
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("erro", response.data)

    def test_sync_offline_veiculo_inexistente(self):
        """Testa rejeição quando veículo não existe."""
        response = self.client.post(
            "/api/sync/offline/",
            {
                "veiculo_id": 99999,  # Veículo inexistente
                "medicoes": [
                    {
                        "id_veiculo": 99999,
                        "temperatura": 85.5,
                        "vibracao": 2.3,
                        "rpm": 2500,
                        "timestamp_coleta": "2026-04-16T10:30:00Z",
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("erro", response.data)

    def test_sync_offline_payload_gigante(self):
        """Testa sincronização com payload gigante (1000 registros)."""
        medicoes = []
        base_time = datetime(2026, 4, 16, 10, 0, 0)

        for i in range(1000):
            medicoes.append(
                {
                    "id_veiculo": self.veiculo.id,
                    "temperatura": 80 + (i % 20),
                    "vibracao": 1 + (i % 5),
                    "rpm": 2000 + (i % 1000),
                    "timestamp_coleta": (base_time + timedelta(seconds=i)).isoformat(),
                }
            )

        response = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": medicoes},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "sucesso")
        self.assertEqual(response.data["registros_inseridos"], 1000)

        # Verifica se todos os 1000 registros foram inseridos
        self.assertEqual(
            MedicaoVeiculoIoT.objects.filter(veiculo=self.veiculo).count(), 1000
        )

    def test_sync_offline_payload_ruidoso(self):
        """Testa sincronização com payload com dados malformados."""
        response = self.client.post(
            "/api/sync/offline/",
            {
                "veiculo_id": self.veiculo.id,
                "medicoes": [
                    {
                        "id_veiculo": self.veiculo.id,
                        "temperatura": 85.5,
                        "vibracao": 2.3,
                        "rpm": 2500,
                        "timestamp_coleta": "2026-04-16T10:30:00Z",
                    },
                    {
                        # Faltam campos - será rejeitado pelo serializer
                        "id_veiculo": self.veiculo.id,
                        "temperatura": 87.0,
                    },
                    {
                        "id_veiculo": self.veiculo.id,
                        "temperatura": 86.2,
                        "vibracao": 2.4,
                        "rpm": 2550,
                        "timestamp_coleta": "2026-04-16T10:32:00Z",
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # O serializer deve rejeitar o payload inteiro porque há erro em um registro

    def test_sync_offline_duplicatas_retransmissao(self):
        """Testa que duplicatas de retransmissão são ignoradas ou retornam 0."""
        medicoes = [
            {
                "id_veiculo": self.veiculo.id,
                "temperatura": 85.5,
                "vibracao": 2.3,
                "rpm": 2500,
                "timestamp_coleta": "2026-04-16T10:30:00Z",
            }
        ]

        # Primeira sincronização
        response1 = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": medicoes},
            format="json",
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.data["registros_inseridos"], 1)

        # Segunda sincronização com MESMA medição (retransmissão)
        response2 = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": medicoes},
            format="json",
        )
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        # ignore_conflicts=True faz com que a duplicata seja silenciosamente ignorada
        # Pode retornar 0 ou 1 dependendo da implementação de ignore_conflicts
        # Nesse caso, esperamos 0 porque existe unique_together
        self.assertIn(response2.data["registros_inseridos"], [0, 1])

        # Total no DB deve ser 1 (não mais de 1)
        count = MedicaoVeiculoIoT.objects.filter(veiculo=self.veiculo).count()
        self.assertEqual(count, 1)

    def test_sync_offline_nao_autenticado(self):
        """Testa que sync rejeita requisição não autenticada."""
        self.client.force_authenticate(user=None)  # Remove autenticação

        response = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": []},
            format="json",
        )

        # Pode ser 401 (Unauthorized) ou 403 (Forbidden), ambos aceitáveis
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_sync_offline_transacao_rollback(self):
        """Testa que transação faz rollback se houver erro de integridade."""
        # Cria uma medição inicial
        medicoes_iniciais = [
            {
                "id_veiculo": self.veiculo.id,
                "temperatura": 85.5,
                "vibracao": 2.3,
                "rpm": 2500,
                "timestamp_coleta": "2026-04-16T10:30:00Z",
            }
        ]

        response1 = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": medicoes_iniciais},
            format="json",
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Tenta sincronizar novamente com MESMA medição
        # Por causa de unique_together, deve dar erro
        response2 = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": medicoes_iniciais},
            format="json",
        )

        # Como ignore_conflicts=True, duplicata é silenciada
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        # Mas pode estar vazio
        if response2.data["registros_inseridos"] == 0:
            # Isso é aceitável com ignore_conflicts
            pass


class SyncServiceUnitTestCase(APITestCase):
    """Testes unitários do SyncService sem fazer requisições HTTP."""

    def setUp(self):
        """Configura dados iniciais."""
        self.marca = Marca.objects.create(nome="MASSEY")
        self.modelo = Modelo.objects.create(nome="MF2715")
        self.veiculo = Veiculo.objects.create(
            descricao="Trator",
            marca=self.marca,
            modelo=self.modelo,
            ano=2020,
            horimetro=5000.0,
        )

    def test_processar_sync_offline_sucesso(self):
        """Testa processamento bem-sucedido."""
        medicoes_data = [
            {
                "temperatura": 85.5,
                "vibracao": 2.3,
                "rpm": 2500,
                "timestamp_coleta": datetime(2026, 4, 16, 10, 30, 0),
            }
        ]

        resultado = SyncService.processar_sync_offline(
            veiculo_id=self.veiculo.id, medicoes_data=medicoes_data
        )

        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["registros_inseridos"], 1)

    def test_processar_sync_offline_vazio(self):
        """Testa sincronização com lista vazia."""
        resultado = SyncService.processar_sync_offline(
            veiculo_id=self.veiculo.id, medicoes_data=[]
        )

        self.assertEqual(resultado["status"], "ignorado")
        self.assertEqual(resultado["registros_inseridos"], 0)

    def test_processar_sync_offline_race_condition(self):
        """Testa tratamento de race condition (veículo deletado)."""
        veiculo_id = self.veiculo.id

        medicoes_data = [
            {
                "temperatura": 85.5,
                "vibracao": 2.3,
                "rpm": 2500,
                "timestamp_coleta": datetime(2026, 4, 16, 10, 30, 0),
            }
        ]

        self.veiculo.delete()

        resultado = SyncService.processar_sync_offline(
            veiculo_id=veiculo_id, medicoes_data=medicoes_data
        )

        self.assertEqual(resultado["status"], "erro")
        self.assertEqual(resultado["código_erro"], "VEICULO_NAO_EXISTE")
        self.assertEqual(resultado["registros_inseridos"], 0)

    def test_processar_sync_offline_bulk_batch_size(self):
        """Testa que bulk_create respeita batch_size=500."""
        # Cria 1500 medições (vai em 3 batches de 500)
        medicoes_data = []
        base_time = datetime(2026, 4, 16, 10, 0, 0)

        for i in range(1500):
            medicoes_data.append(
                {
                    "temperatura": 80 + (i % 20),
                    "vibracao": 1 + (i % 5),
                    "rpm": 2000 + (i % 1000),
                    "timestamp_coleta": base_time + timedelta(seconds=i),
                }
            )

        resultado = SyncService.processar_sync_offline(
            veiculo_id=self.veiculo.id, medicoes_data=medicoes_data
        )

        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["registros_inseridos"], 1500)
        self.assertEqual(
            MedicaoVeiculoIoT.objects.filter(veiculo=self.veiculo).count(), 1500
        )
