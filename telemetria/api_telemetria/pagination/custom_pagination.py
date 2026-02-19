"""
Paginação customizada para a API.
Define o padrão de paginação com controle de tamanho de página.
"""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Paginação padrão da API.
    
    - page_size: 10 itens por página (padrão)
    - page_size_query_param: permite ao cliente definir o tamanho via ?page_size=N
    - max_page_size: limite máximo de 100 itens por página
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
