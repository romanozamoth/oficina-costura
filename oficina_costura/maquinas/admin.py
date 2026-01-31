from django.contrib import admin
from servicos.models import OrdemServico
from .models import Maquina

# Register your models here.

class OrdemServicoInline(admin.TabularInline):
    model = OrdemServico
    extra = 0
    readonly_fields = ('status', 'criado_em', 'finalizado_em')

@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'numero_serie', 'cliente')
    search_fields = ('modelo', 'numero_serie', 'cliente__nome')
    list_filter = ('cliente',)
    inlines = [OrdemServicoInline]