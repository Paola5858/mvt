"""
Tratamento customizado de exceções da API.
Padroniza as respostas de erro para melhor experiência do cliente.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Handler customizado para exceções da API.
    
    Retorna respostas padronizadas com estrutura:
    {
        "error": true,
        "message": "Mensagem de erro",
        "details": {...}
    }
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response = {
            'error': True,
            'message': 'Ocorreu um erro na requisição',
            'details': response.data
        }
        response.data = custom_response
    
    return response
