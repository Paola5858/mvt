"""Serializers da API de Telemetria."""
from rest_framework import serializers
from .models import Setor, Sensor, Leitura


class SetorSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Setor.
    
    Responsável por serializar/deserializar dados de setores.
    Inclui contagem de sensores associados.
    """
    total_sensores = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Setor
        fields = ['id', 'nome', 'localizacao', 'total_sensores']
        read_only_fields = ['id']
    
    def get_total_sensores(self, obj):
        """Retorna o total de sensores no setor."""
        return obj.sensores.count()
    
    def validate_nome(self, value):
        """Valida que o nome do setor não seja vazio ou apenas espaços."""
        if not value or not value.strip():
            raise serializers.ValidationError("O nome do setor não pode ser vazio.")
        return value.strip()


class SetorNestedSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado de Setor para uso em relacionamentos nested.
    Evita recursão infinita e melhora performance.
    """
    class Meta:
        model = Setor
        fields = ['id', 'nome', 'localizacao']
        read_only_fields = ['id', 'nome', 'localizacao']


class SensorSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Sensor.
    
    Inclui dados do setor (nested) e contagem de leituras.
    Valida status e tipo do sensor.
    """
    setor_detalhes = SetorNestedSerializer(source='setor', read_only=True)
    total_leituras = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Sensor
        fields = ['id', 'setor', 'setor_detalhes', 'tipo', 'status', 'total_leituras']
        read_only_fields = ['id']
    
    def get_total_leituras(self, obj):
        """Retorna o total de leituras do sensor."""
        return obj.leituras.count()
    
    def validate_status(self, value):
        """Valida que o status seja um dos valores permitidos."""
        status_validos = ['ativo', 'inativo', 'manutenção']
        if value.lower() not in status_validos:
            raise serializers.ValidationError(
                f"Status inválido. Valores permitidos: {', '.join(status_validos)}"
            )
        return value.lower()
    
    def validate_tipo(self, value):
        """Valida que o tipo não seja vazio."""
        if not value or not value.strip():
            raise serializers.ValidationError("O tipo do sensor não pode ser vazio.")
        return value.strip()


class SensorNestedSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado de Sensor para uso em relacionamentos nested.
    """
    class Meta:
        model = Sensor
        fields = ['id', 'tipo', 'status']
        read_only_fields = ['id', 'tipo', 'status']


class LeituraSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Leitura.
    
    Inclui dados do sensor (nested) para facilitar consultas.
    Valida valores de leitura e impede modificação de data_hora.
    """
    sensor_detalhes = SensorNestedSerializer(source='sensor', read_only=True)
    
    class Meta:
        model = Leitura
        fields = ['id', 'sensor', 'sensor_detalhes', 'valor', 'data_hora']
        read_only_fields = ['id', 'data_hora']
    
    def validate_valor(self, value):
        """Valida que o valor da leitura esteja dentro de limites razoáveis."""
        if value < -100 or value > 1000:
            raise serializers.ValidationError(
                "Valor fora do intervalo permitido (-100 a 1000)."
            )
        return value
