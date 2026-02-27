from rest_framework import serializers
from .models import TipoSanguineo, Doador

class TipoSanguineoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSanguineo
        fields = '__all__'

class DoadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doador
        fields = '__all__'
