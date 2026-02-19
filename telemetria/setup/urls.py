"""URLs da API de Telemetria."""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api_telemetria.viewsets import SetorViewSet, SensorViewSet, LeituraViewSet

# Router da API v1
router_v1 = DefaultRouter()
router_v1.register(r"setores", SetorViewSet, basename='setor')
router_v1.register(r"sensores", SensorViewSet, basename='sensor')
router_v1.register(r"leituras", LeituraViewSet, basename='leitura')

# Swagger/OpenAPI Schema
schema_view = get_schema_view(
    openapi.Info(
        title="API Telemetria",
        default_version="v1",
        description="""API REST para gerenciamento de telemetria agrícola.
        
        ## Funcionalidades
        - Gerenciamento de Setores
        - Gerenciamento de Sensores
        - Registro e consulta de Leituras
        - Filtros avançados por data, sensor e valores
        - Paginação e ordenação de resultados
        - Autenticação por Token
        
        ## Versionamento
        Esta é a versão 1 da API (v1).
        
        ## Autenticação
        Use Token Authentication para operações de escrita.
        Leitura é pública (IsAuthenticatedOrReadOnly).
        """,
        contact=openapi.Contact(email="contato@telemetria.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # API v1 com versionamento
    path("api/v1/", include((router_v1.urls, 'v1'), namespace='v1')),
    
    # Autenticação
    path("api/v1/auth/token/", obtain_auth_token, name='api-token-auth'),
    
    # Documentação Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name='schema-redoc'),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
