"""Testes da API de Telemetria de Veículos."""
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Marca, Modelo, Veiculo, UnidadeMedida, Medicao, MedicaoVeiculo


class MarcaTestCase(APITestCase):
    """Testes para o endpoint de Marcas."""
    
    def test_criar_marca(self):
        """Testa a criação de uma marca."""
        response = self.client.post('/api/marcas/', {'nome': 'FIAT'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], 'FIAT')
    
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
        response = self.client.post('/api/modelos/', {'nome': 'UNO'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], 'UNO')


class VeiculoTestCase(APITestCase):
    """Testes para o endpoint de Veículos."""
    
    def setUp(self):
        """Configura dados iniciais para os testes."""
        self.marca = Marca.objects.create(nome='FIAT')
        self.modelo = Modelo.objects.create(nome='UNO')
    
    def test_criar_veiculo(self):
        """Testa a criação de um veículo."""
        data = {
            'descricao': 'Carro de teste',
            'marca': self.marca.id,
            'modelo': self.modelo.id,
            'ano': 2022,
            'horimetro': 5000.0
        }
        response = self.client.post('/api/veiculos/', data, format='json')
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
        self.marca = Marca.objects.create(nome='FIAT')
        self.modelo = Modelo.objects.create(nome='UNO')
        self.veiculo = Veiculo.objects.create(
            descricao='Veículo Teste',
            marca=self.marca,
            modelo=self.modelo,
            ano=2020,
            horimetro=10000.0
        )
        self.unidade = UnidadeMedida.objects.create(nome='Horas')
        self.medicao = Medicao.objects.create(
            tipo='horimetro',
            unidade_medida=self.unidade
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
