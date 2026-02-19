from rest_framework import viewsets
from .models import Marca, Modelo, Veiculo, UnidadeMedida, Medicao, MedicaoVeiculo
from .serializers import (
    MarcaSerializer, ModeloSerializer, VeiculoSerializer,
    UnidadeMedidaSerializer, MedicaoSerializer, MedicaoVeiculoSerializer
)


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer


class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.select_related('marca', 'modelo').all()
    serializer_class = VeiculoSerializer


class UnidadeMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadeMedida.objects.all()
    serializer_class = UnidadeMedidaSerializer


class MedicaoViewSet(viewsets.ModelViewSet):
    queryset = Medicao.objects.select_related('unidade_medida').all()
    serializer_class = MedicaoSerializer


class MedicaoVeiculoViewSet(viewsets.ModelViewSet):
    queryset = MedicaoVeiculo.objects.select_related('veiculo', 'medicao').all()
    serializer_class = MedicaoVeiculoSerializer
