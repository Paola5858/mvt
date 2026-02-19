"""Configuração do Django Admin para a API de Telemetria."""
from django.contrib import admin
from .models import Setor, Sensor, Leitura


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    """Admin customizado para Setores."""
    list_display = ['id', 'nome', 'localizacao', 'total_sensores']
    search_fields = ['nome', 'localizacao']
    list_filter = ['nome']
    
    def total_sensores(self, obj):
        """Exibe o total de sensores no setor."""
        return obj.sensores.count()
    total_sensores.short_description = 'Total de Sensores'


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    """Admin customizado para Sensores."""
    list_display = ['id', 'tipo', 'setor', 'status', 'total_leituras']
    search_fields = ['tipo', 'setor__nome']
    list_filter = ['status', 'setor']
    list_select_related = ['setor']
    
    def total_leituras(self, obj):
        """Exibe o total de leituras do sensor."""
        return obj.leituras.count()
    total_leituras.short_description = 'Total de Leituras'


@admin.register(Leitura)
class LeituraAdmin(admin.ModelAdmin):
    """Admin customizado para Leituras."""
    list_display = ['id', 'sensor', 'valor']
    search_fields = ['sensor__tipo']
    list_filter = ['sensor']
    list_select_related = ['sensor', 'sensor__setor']
