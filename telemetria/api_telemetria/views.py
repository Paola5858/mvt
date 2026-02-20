from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Marca, Modelo, Veiculo, UnidadeMedida, Medicao, MedicaoVeiculo
from .serializers import (
    MarcaSerializer, ModeloSerializer, VeiculoSerializer,
    UnidadeMedidaSerializer, MedicaoSerializer, MedicaoVeiculoSerializer
)


class MarcaViewSet(viewsets.ModelViewSet):
    """ViewSet com busca e ordenação."""
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'id']
    ordering = ['nome']


class ModeloViewSet(viewsets.ModelViewSet):
    """ViewSet com busca e ordenação."""
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'id']
    ordering = ['nome']


class VeiculoViewSet(viewsets.ModelViewSet):
    """ViewSet com filtros, busca e ordenação."""
    queryset = Veiculo.objects.select_related('marca', 'modelo').all()
    serializer_class = VeiculoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['marca', 'modelo', 'ano']
    search_fields = ['descricao', 'marca__nome', 'modelo__nome']
    ordering_fields = ['ano', 'horimetro', 'id']
    ordering = ['-ano']


class UnidadeMedidaViewSet(viewsets.ModelViewSet):
    """ViewSet com busca."""
    queryset = UnidadeMedida.objects.all()
    serializer_class = UnidadeMedidaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']


class MedicaoViewSet(viewsets.ModelViewSet):
    """ViewSet com filtros e busca."""
    queryset = Medicao.objects.select_related('unidade_medida').all()
    serializer_class = MedicaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tipo', 'unidade_medida']
    search_fields = ['tipo']


class MedicaoVeiculoViewSet(viewsets.ModelViewSet):
    """ViewSet com filtros avançados, busca e ordenação."""
    queryset = MedicaoVeiculo.objects.select_related('veiculo', 'medicao').all()
    serializer_class = MedicaoVeiculoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['veiculo', 'medicao', 'data']
    search_fields = ['veiculo__descricao']
    ordering_fields = ['data', 'valor']
    ordering = ['-data']
