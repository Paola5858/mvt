from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Setor, Sensor, Leitura
from .serializers import SetorSerializer, SensorSerializer, LeituraSerializer


class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class LeituraViewSet(viewsets.ModelViewSet):
    queryset = Leitura.objects.all()
    serializer_class = LeituraSerializer
