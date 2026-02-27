from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import TipoSanguineo, Doador
from .serializers import TipoSanguineoSerializer, DoadorSerializer, DoadorListSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TipoSanguineoViewSet(viewsets.ModelViewSet):
    queryset = TipoSanguineo.objects.all()
    serializer_class = TipoSanguineoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['tipo']

class DoadorViewSet(viewsets.ModelViewSet):
    queryset = Doador.objects.select_related('tipo_sanguineo').all()
    serializer_class = DoadorSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_sanguineo', 'ativo']
    search_fields = ['nome', 'email', 'cpf']
    ordering_fields = ['nome', 'criado_em', 'ultima_doacao']
    ordering = ['-criado_em']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DoadorListSerializer
        return DoadorSerializer
