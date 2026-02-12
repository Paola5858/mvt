from rest_framework import serializers
from .models import Talhao

class TalhaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talhao
        fields = '__all__'
