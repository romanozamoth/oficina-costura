from django.contrib import admin
from django.utils import timezone
from django.utils.timezone import now
from datetime import date
from .models import OrdemServico, ComentarioOS


class ComentarioOSInline(admin.TabularInline):
    model = ComentarioOS
    extra = 1
    readonly_fields = ('autor', 'criado_em')

    def save_model(self, request, obj, form, change):
        if not obj.autor:
            obj.autor = request.user
        super().save_model(request, obj, form, change)


@admin.action(description='Marcar como Em andamento')
def marcar_em_andamento(modeladmin, request, queryset):
    queryset.filter(
        status=OrdemServico.Status.ABERTO
    ).update(
        status=OrdemServico.Status.EM_ANDAMENTO
    )

@admin.action(description='Finalizar Ordem de Serviço')
def finalizar_os(modeladmin, request, queryset):
    queryset.filter(
        status=OrdemServico.Status.EM_ANDAMENTO
    ).update(
        status=OrdemServico.Status.FINALIZADO,
        finalizado_em=timezone.now()
    )

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    change_list_template = "admin/servicos/dashboard.html"
    
    list_display = (
        'id',
        'status',
        'descricao_problema',
        'maquina',
        'criado_em',
        'finalizado_em'
    )

    list_filter = ('status', 'criado_em')
    search_fields = (
        'maquina__modelo',
        'descricao_problema'
    )
    
    ordering = ('-criado_em',)

    actions = [marcar_em_andamento, finalizar_os]

    readonly_fields = ('criado_em', 'finalizado_em')

    fieldsets = (
        ('Máquina', {
            'fields': ('maquina',)
        }),
        ('Detalhes do Problema', {
            'fields': ('descricao_problema',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Datas', {
            'fields': ('criado_em', 'finalizado_em')
        }),
    )

    inlines = [ComentarioOSInline]

    def save_model(self, request, obj, form, change):
        if obj.status == obj.Status.FINALIZADO and obj.finalizado_em is None:
            obj.finalizado_em = timezone.now()

        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context['abertas'] = OrdemServico.objects.filter(
            status=OrdemServico.Status.ABERTO
        ).count()

        extra_context['andamento'] = OrdemServico.objects.filter(
            status=OrdemServico.Status.EM_ANDAMENTO
        ).count()

        extra_context['finalizadas'] = OrdemServico.objects.filter(
            status=OrdemServico.Status.FINALIZADO
        ).count()

        extra_context['finalizadas_hoje'] = OrdemServico.objects.filter(
            status=OrdemServico.Status.FINALIZADO,
            finalizado_em__date=date.today()
        ).count()

        return super().changelist_view(request, extra_context=extra_context)
