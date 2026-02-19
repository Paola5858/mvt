"""URLs da API de Telemetria de Veículos."""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api_telemetria.views import (
    MarcaViewSet, ModeloViewSet, VeiculoViewSet,
    UnidadeMedidaViewSet, MedicaoViewSet, MedicaoVeiculoViewSet
)

# Router da API
router = DefaultRouter()
router.register(r"marcas", MarcaViewSet, basename='marca')
router.register(r"modelos", ModeloViewSet, basename='modelo')
router.register(r"veiculos", VeiculoViewSet, basename='veiculo')
router.register(r"unidades-medida", UnidadeMedidaViewSet, basename='unidademedida')
router.register(r"medicoes", MedicaoViewSet, basename='medicao')
router.register(r"medicoes-veiculo", MedicaoVeiculoViewSet, basename='medicaoveiculo')

# Swagger/OpenAPI Schema
schema_view = get_schema_view(
    openapi.Info(
        title="API Telemetria de Veículos",
        default_version="v1",
        description="""API REST para gerenciamento de telemetria de veículos.
        
        ## Funcionalidades
        - Gerenciamento de Marcas e Modelos
        - Cadastro de Veículos
        - Registro de Medições (Horímetro, Odômetro, Combustível)
        - Unidades de Medida
        - Histórico de Medições por Veículo
        """,
        contact=openapi.Contact(email="contato@telemetria.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name='schema-redoc'),
]
