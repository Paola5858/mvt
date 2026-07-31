"""Testes de endpoints HTTP da API de Telemetria."""
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime, timedelta
from django.contrib.auth.models import User

from api_telemetria.models import (
    Marca,
    Modelo,
    Veiculo,
    UnidadeMedida,
    Medicao,
    MedicaoVeiculoIoT,
)


class MarcaTestCase(APITestCase):
    def test_criar_marca(self):
        response = self.client.post("/api/marcas/", {"nome": "FIAT"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome"], "FIAT")  # type: ignore

    def test_listar_marcas(self):
        Marca.objects.create(nome="FIAT")
        Marca.objects.create(nome="VW")
        response = self.client.get("/api/marcas/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ModeloTestCase(APITestCase):
    def test_criar_modelo(self):
        response = self.client.post("/api/modelos/", {"nome": "UNO"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome"], "UNO")  # type: ignore


class VeiculoTestCase(APITestCase):
    def setUp(self):
        self.marca = Marca.objects.create(nome="FIAT")
        self.modelo = Modelo.objects.create(nome="UNO")

    def test_criar_veiculo(self):
        data = {
            "descricao": "Carro de teste",
            "marca": self.marca.id,  # type: ignore
            "modelo": self.modelo.id,  # type: ignore
            "ano": 2022,
            "horimetro": 5000.0,
        }
        response = self.client.post("/api/veiculos/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_validacao_ano_invalido(self):
        data = {
            "descricao": "Carro",
            "marca": self.marca.id,  # type: ignore
            "modelo": self.modelo.id,  # type: ignore
            "ano": 1800,
            "horimetro": 0,
        }
        response = self.client.post("/api/veiculos/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MedicaoVeiculoTestCase(APITestCase):
    def setUp(self):
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
        self.medicao = Medicao.objects.create(tipo="horimetro", unidade_medida=self.unidade)

    def test_criar_medicao_veiculo(self):
        data = {
            "veiculo": self.veiculo.id,  # type: ignore
            "medicao": self.medicao.id,  # type: ignore
            "data": "2024-01-15",
            "valor": 15000.0,
        }
        response = self.client.post("/api/medicoes-veiculo/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data["valor"]), 15000.0)  # type: ignore


class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="senha123")

    def test_login_retorna_access_e_refresh(self):
        response = self.client.post(
            "/api/auth/login/",
            {"username": "joao", "password": "senha123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertNotIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], "joao")  # type: ignore

    def test_refresh_gera_novo_access(self):
        login_response = self.client.post(
            "/api/auth/login/",
            {"username": "joao", "password": "senha123"},
            format="json",
        )

        refresh_response = self.client.post(
            "/api/auth/refresh/",
            {"refresh": login_response.data["refresh"]},
            format="json",
        )

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)



class SyncOfflineViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="trator", password="tractorpass123")
        self.client.force_authenticate(user=self.user)  # type: ignore
        self.marca = Marca.objects.create(nome="MASSEY")
        self.modelo = Modelo.objects.create(nome="MF2715")
        self.veiculo = Veiculo.objects.create(
            descricao="Trator sem internet",
            marca=self.marca,
            modelo=self.modelo,
            ano=2020,
            horimetro=5000.0,
        )

    def _medicao(self, ts="2026-04-16T10:30:00Z", **kwargs):
        return {
            "id_veiculo": self.veiculo.id,  # type: ignore
            "temperatura": 85.5,
            "vibracao": 2.3,
            "rpm": 2500,
            "timestamp_coleta": ts,
            **kwargs,
        }

    def test_payload_valido(self):
        response = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": [self._medicao(), self._medicao("2026-04-16T10:31:00Z")]},  # type: ignore
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["registros_inseridos"], 2)  # type: ignore
        self.assertEqual(MedicaoVeiculoIoT.objects.filter(veiculo=self.veiculo).count(), 2)

    def test_temperatura_invalida(self):
        response = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": [self._medicao(temperatura=300)]},  # type: ignore
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vibracao_invalida(self):
        response = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": [self._medicao(vibracao=150)]},  # type: ignore
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rpm_invalido(self):
        response = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": [self._medicao(rpm=15000)]},  # type: ignore
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_veiculo_inexistente(self):
        response = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": 99999, "medicoes": [self._medicao()]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payload_gigante(self):
        base = datetime(2026, 4, 16, 10, 0, 0)
        medicoes = [
            self._medicao(
                ts=(base + timedelta(seconds=i)).isoformat(),
                temperatura=80 + (i % 20),
                vibracao=1 + (i % 5),
                rpm=2000 + (i % 1000),
            )
            for i in range(1000)
        ]
        response = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": medicoes},  # type: ignore
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["registros_inseridos"], 1000)  # type: ignore

    def test_payload_ruidoso(self):
        response = self.client.post(
            "/api/sync/offline/",
            {
                "veiculo_id": self.veiculo.id,  # type: ignore
                "medicoes": [
                    self._medicao(),
                    {"id_veiculo": self.veiculo.id, "temperatura": 87.0},  # incompleto  # type: ignore
                    self._medicao("2026-04-16T10:32:00Z"),
                ],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicatas_ignoradas(self):
        payload = {"veiculo_id": self.veiculo.id, "medicoes": [self._medicao()]}  # type: ignore
        self.client.post("/api/sync/offline/", payload, format="json")
        response2 = self.client.post("/api/sync/offline/", payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertIn(response2.data["registros_inseridos"], [0, 1])  # type: ignore
        self.assertEqual(MedicaoVeiculoIoT.objects.filter(veiculo=self.veiculo).count(), 1)

    def test_nao_autenticado(self):
        self.client.force_authenticate(user=None)  # type: ignore
        response = self.client.post(
            "/api/sync/offline/",
            {"veiculo_id": self.veiculo.id, "medicoes": []},  # type: ignore
            format="json",
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
