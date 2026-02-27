from django.contrib import admin
from .models import TipoSanguineo, Doador

@admin.register(TipoSanguineo)
class TipoSanguineoAdmin(admin.ModelAdmin):
    list_display = ['tipo']
    search_fields = ['tipo']

@admin.register(Doador)
class DoadorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_sanguineo', 'email', 'telefone', 'ultima_doacao', 'ativo']
    list_filter = ['tipo_sanguineo', 'ativo', 'ultima_doacao']
    search_fields = ['nome', 'email', 'cpf']
    date_hierarchy = 'criado_em'
    readonly_fields = ['criado_em', 'atualizado_em']
