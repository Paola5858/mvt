"""Serializers da API de Telemetria de Veículos."""
from rest_framework import serializers
from .models import Marca, Modelo, Veiculo, UnidadeMedida, Medicao, MedicaoVeiculo


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nome']
    
    def validate_nome(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O nome da marca não pode ser vazio.")
        if len(value) < 2:
            raise serializers.ValidationError("O nome da marca deve ter pelo menos 2 caracteres.")
        return value.strip().upper()


class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = ['id', 'nome']
    
    def validate_nome(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O nome do modelo não pode ser vazio.")
        if len(value) < 2:
            raise serializers.ValidationError("O nome do modelo deve ter pelo menos 2 caracteres.")
        return value.strip().upper()


class VeiculoSerializer(serializers.ModelSerializer):
    marca_nome = serializers.CharField(source='marca.nome', read_only=True)
    modelo_nome = serializers.CharField(source='modelo.nome', read_only=True)
    
    class Meta:
        model = Veiculo
        fields = ['id', 'descricao', 'marca', 'marca_nome', 'modelo', 'modelo_nome', 'ano', 'horimetro']
    
    def validate_ano(self, value):
        if value < 1900 or value > 2030:
            raise serializers.ValidationError("O ano deve estar entre 1900 e 2030.")
        return value
    
    def validate_horimetro(self, value):
        if value < 0:
            raise serializers.ValidationError("O horímetro não pode ser negativo.")
        if value > 999999:
            raise serializers.ValidationError("O horímetro não pode exceder 999999.")
        return value
    
    def validate_descricao(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("A descrição não pode ser vazia.")
        return value.strip()


class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = ['id', 'nome']
    
    def validate_nome(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O nome da unidade não pode ser vazio.")
        return value.strip()


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
    
    def validate_valor(self, value):
        if value < 0:
            raise serializers.ValidationError("O valor não pode ser negativo.")
        if value > 9999999:
            raise serializers.ValidationError("O valor não pode exceder 9999999.")
        return value
