from django.contrib import admin
from .models import Cliente
from maquinas.models import Maquina

# Register your models here.
class MaquinaInline(admin.TabularInline):
    model = Maquina
    extra = 1

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'endereco', 'criado_em')
    search_fields = ('nome', 'telefone')
    inlines = [MaquinaInline]