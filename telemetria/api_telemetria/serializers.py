"""Serializers da API de Telemetria de Veículos."""
from rest_framework import serializers
from .models import Marca, Modelo, Veiculo, UnidadeMedida, Medicao, MedicaoVeiculo


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nome']


class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = ['id', 'nome']


class VeiculoSerializer(serializers.ModelSerializer):
    marca_nome = serializers.CharField(source='marca.nome', read_only=True)
    modelo_nome = serializers.CharField(source='modelo.nome', read_only=True)
    
    class Meta:
        model = Veiculo
        fields = ['id', 'descricao', 'marca', 'marca_nome', 'modelo', 'modelo_nome', 'ano', 'horimetro']


class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = ['id', 'nome']


class MedicaoSerializer(serializers.ModelSerializer):
    unidade_nome = serializers.CharField(source='unidade_medida.nome', read_only=True)
    
    class Meta:
        model = Medicao
        fields = ['id', 'tipo', 'unidade_medida', 'unidade_nome']


class MedicaoVeiculoSerializer(serializers.ModelSerializer):
    veiculo_descricao = serializers.CharField(source='veiculo.descricao', read_only=True)
    medicao_tipo = serializers.CharField(source='medicao.tipo', read_only=True)
    
    class Meta:
        model = MedicaoVeiculo
        fields = ['id', 'veiculo', 'veiculo_descricao', 'medicao', 'medicao_tipo', 'data', 'valor']
