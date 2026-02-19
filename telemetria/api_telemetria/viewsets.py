"""ViewSets da API de Telemetria."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Setor, Sensor, Leitura
from .serializers import SetorSerializer, SensorSerializer, LeituraSerializer
from .filters import LeituraFilter
from .pagination import StandardResultsSetPagination


class SetorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Setores.
    
    Permite operações CRUD completas em setores.
    Inclui busca por nome e localização.
    """
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'localizacao']
    ordering_fields = ['nome', 'id']
    ordering = ['nome']
    
    @swagger_auto_schema(
        operation_description="Lista todos os setores cadastrados",
        operation_summary="Listar setores",
        tags=['Setores']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Cria um novo setor",
        operation_summary="Criar setor",
        tags=['Setores']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Retorna detalhes de um setor específico",
        operation_summary="Detalhar setor",
        tags=['Setores']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Atualiza todos os campos de um setor",
        operation_summary="Atualizar setor (completo)",
        tags=['Setores']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Atualiza parcialmente um setor",
        operation_summary="Atualizar setor (parcial)",
        tags=['Setores']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Remove um setor do sistema",
        operation_summary="Deletar setor",
        tags=['Setores']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        method='get',
        operation_description="Lista todos os sensores de um setor específico",
        operation_summary="Listar sensores do setor",
        tags=['Setores'],
        responses={200: SensorSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def sensores(self, request, pk=None):
        """Retorna todos os sensores de um setor."""
        setor = self.get_object()
        sensores = setor.sensores.all()
        serializer = SensorSerializer(sensores, many=True)
        return Response(serializer.data)


class SensorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Sensores.
    
    Permite operações CRUD completas em sensores.
    Inclui filtros por setor e status, busca por tipo.
    """
    queryset = Sensor.objects.select_related('setor').all()
    serializer_class = SensorSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['setor', 'status']
    search_fields = ['tipo']
    ordering_fields = ['id', 'tipo']
    ordering = ['id']
    
    @swagger_auto_schema(
        operation_description="Lista todos os sensores cadastrados. Permite filtrar por setor e status.",
        operation_summary="Listar sensores",
        tags=['Sensores'],
        manual_parameters=[
            openapi.Parameter('setor', openapi.IN_QUERY, description="ID do setor", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY, description="Status do sensor", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Cria um novo sensor",
        operation_summary="Criar sensor",
        tags=['Sensores']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Retorna detalhes de um sensor específico",
        operation_summary="Detalhar sensor",
        tags=['Sensores']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Atualiza todos os campos de um sensor",
        operation_summary="Atualizar sensor (completo)",
        tags=['Sensores']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Atualiza parcialmente um sensor",
        operation_summary="Atualizar sensor (parcial)",
        tags=['Sensores']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Remove um sensor do sistema",
        operation_summary="Deletar sensor",
        tags=['Sensores']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        method='get',
        operation_description="Lista todas as leituras de um sensor específico",
        operation_summary="Listar leituras do sensor",
        tags=['Sensores'],
        responses={200: LeituraSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def leituras(self, request, pk=None):
        """Retorna todas as leituras de um sensor."""
        sensor = self.get_object()
        leituras = sensor.leituras.all().order_by('-data_hora')
        page = self.paginate_queryset(leituras)
        if page is not None:
            serializer = LeituraSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = LeituraSerializer(leituras, many=True)
        return Response(serializer.data)


class LeituraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Leituras.
    
    Permite operações CRUD completas em leituras.
    Inclui filtros avançados por sensor, data e valor.
    Ordenação por data (mais recentes primeiro).
    """
    queryset = Leitura.objects.select_related('sensor', 'sensor__setor').all()
    serializer_class = LeituraSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = LeituraFilter
    ordering_fields = ['data_hora', 'valor']
    ordering = ['-data_hora']
    
    @swagger_auto_schema(
        operation_description="Lista todas as leituras. Permite filtrar por sensor, intervalo de datas e valores.",
        operation_summary="Listar leituras",
        tags=['Leituras'],
        manual_parameters=[
            openapi.Parameter('sensor', openapi.IN_QUERY, description="ID do sensor", type=openapi.TYPE_INTEGER),
            openapi.Parameter('data_inicio', openapi.IN_QUERY, description="Data inicial (YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('data_fim', openapi.IN_QUERY, description="Data final (YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('valor_min', openapi.IN_QUERY, description="Valor mínimo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('valor_max', openapi.IN_QUERY, description="Valor máximo", type=openapi.TYPE_NUMBER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Cria uma nova leitura",
        operation_summary="Criar leitura",
        tags=['Leituras']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Retorna detalhes de uma leitura específica",
        operation_summary="Detalhar leitura",
        tags=['Leituras']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Atualiza todos os campos de uma leitura",
        operation_summary="Atualizar leitura (completo)",
        tags=['Leituras']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Atualiza parcialmente uma leitura",
        operation_summary="Atualizar leitura (parcial)",
        tags=['Leituras']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Remove uma leitura do sistema",
        operation_summary="Deletar leitura",
        tags=['Leituras']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
