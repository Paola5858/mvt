"""
Filtros personalizados para o modelo Leitura.
Permite filtrar leituras por sensor, intervalo de datas e valores.
"""
from django_filters import rest_framework as filters
from api_telemetria.models import Leitura


class LeituraFilter(filters.FilterSet):
    """
    Filtro avançado para leituras de sensores.
    
    Filtros disponíveis:
    - sensor: ID do sensor
    - data_inicio: Data inicial (formato: YYYY-MM-DD)
    - data_fim: Data final (formato: YYYY-MM-DD)
    - valor_min: Valor mínimo da leitura
    - valor_max: Valor máximo da leitura
    """
    data_inicio = filters.DateTimeFilter(field_name='data_hora', lookup_expr='gte')
    data_fim = filters.DateTimeFilter(field_name='data_hora', lookup_expr='lte')
    valor_min = filters.NumberFilter(field_name='valor', lookup_expr='gte')
    valor_max = filters.NumberFilter(field_name='valor', lookup_expr='lte')
    
    class Meta:
        model = Leitura
        fields = ['sensor', 'data_inicio', 'data_fim', 'valor_min', 'valor_max']
