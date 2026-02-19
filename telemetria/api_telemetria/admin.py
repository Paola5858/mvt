"""Configuração do Django Admin para a API de Telemetria de Veículos."""
from django.contrib import admin
from .models import Marca, Modelo, Veiculo, UnidadeMedida, Medicao, MedicaoVeiculo


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'marca', 'modelo', 'ano', 'horimetro']
    search_fields = ['descricao', 'marca__nome', 'modelo__nome']
    list_filter = ['marca', 'modelo', 'ano']
    list_select_related = ['marca', 'modelo']


@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']


@admin.register(Medicao)
class MedicaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'unidade_medida']
    search_fields = ['tipo']
    list_filter = ['tipo', 'unidade_medida']
    list_select_related = ['unidade_medida']


@admin.register(MedicaoVeiculo)
class MedicaoVeiculoAdmin(admin.ModelAdmin):
    list_display = ['id', 'veiculo', 'medicao', 'data', 'valor']
    search_fields = ['veiculo__descricao']
    list_filter = ['medicao', 'data']
    list_select_related = ['veiculo', 'medicao']
