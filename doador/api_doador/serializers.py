from rest_framework import serializers
from .models import TipoSanguineo, Doador

class TipoSanguineoSerializer(serializers.ModelSerializer):
    total_doadores = serializers.SerializerMethodField()
    
    class Meta:
        model = TipoSanguineo
        fields = ['id', 'tipo', 'total_doadores']
    
    def get_total_doadores(self, obj):
        return obj.doadores.filter(ativo=True).count()

class DoadorSerializer(serializers.ModelSerializer):
    tipo_sanguineo_display = serializers.CharField(source='tipo_sanguineo.tipo', read_only=True)
    
    class Meta:
        model = Doador
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

class DoadorListSerializer(serializers.ModelSerializer):
    tipo_sanguineo = serializers.CharField(source='tipo_sanguineo.tipo')
    
    class Meta:
        model = Doador
        fields = ['id', 'nome', 'tipo_sanguineo', 'email', 'telefone', 'ultima_doacao', 'ativo']
