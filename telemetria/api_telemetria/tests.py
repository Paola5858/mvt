"""Testes automatizados da API de Telemetria."""
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Setor, Sensor, Leitura


class SetorTestCase(APITestCase):
    """Testes para o endpoint de Setores."""
    
    def setUp(self):
        """Cria usuário para autenticação."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
    
    def test_criar_setor(self):
        """Testa a criação de um setor."""
        url = reverse('v1:setor-list')
        data = {'nome': 'Estufa 1', 'localizacao': 'Área Norte'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Setor.objects.count(), 1)
        self.assertEqual(response.data['nome'], 'Estufa 1')
    
    def test_listar_setores(self):
        """Testa a listagem de setores."""
        Setor.objects.create(nome='Estufa 1', localizacao='Norte')
        Setor.objects.create(nome='Estufa 2', localizacao='Sul')
        
        url = reverse('v1:setor-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)


class SensorTestCase(APITestCase):
    """Testes para o endpoint de Sensores."""
    
    def setUp(self):
        """Configura dados iniciais para os testes."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.setor = Setor.objects.create(nome='Estufa 1', localizacao='Norte')
    
    def test_criar_sensor(self):
        """Testa a criação de um sensor."""
        url = reverse('v1:sensor-list')
        data = {
            'setor': self.setor.id,
            'tipo': 'Temperatura',
            'status': 'ativo'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sensor.objects.count(), 1)
        self.assertEqual(response.data['tipo'], 'Temperatura')
        self.assertIn('setor_detalhes', response.data)
    
    def test_validacao_status_sensor(self):
        """Testa validação de status inválido."""
        url = reverse('v1:sensor-list')
        data = {
            'setor': self.setor.id,
            'tipo': 'Temperatura',
            'status': 'quebrado'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LeituraTestCase(APITestCase):
    """Testes para o endpoint de Leituras."""
    
    def setUp(self):
        """Configura dados iniciais para os testes."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.setor = Setor.objects.create(nome='Estufa 1', localizacao='Norte')
        self.sensor = Sensor.objects.create(
            setor=self.setor,
            tipo='Temperatura',
            status='ativo'
        )
    
    def test_criar_leitura(self):
        """Testa a criação de uma leitura."""
        url = reverse('v1:leitura-list')
        data = {'sensor': self.sensor.id, 'valor': 25.5}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Leitura.objects.count(), 1)
        self.assertEqual(float(response.data['valor']), 25.5)
        self.assertIn('sensor_detalhes', response.data)
    
    def test_filtro_leitura_por_sensor(self):
        """Testa filtro de leituras por sensor."""
        Leitura.objects.create(sensor=self.sensor, valor=25.5)
        Leitura.objects.create(sensor=self.sensor, valor=26.0)
        
        url = reverse('v1:leitura-list')
        response = self.client.get(url, {'sensor': self.sensor.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_validacao_valor_leitura(self):
        """Testa validação de valor fora do intervalo."""
        url = reverse('v1:leitura-list')
        data = {'sensor': self.sensor.id, 'valor': 1500}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
