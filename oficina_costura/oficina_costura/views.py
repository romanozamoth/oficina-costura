from django.shortcuts import render
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import date
from servicos.models import OrdemServico, PecaOS
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

def dashboard(request):
    now = timezone.now()

    faturamento_mensal = (
        OrdemServico.objects
        .filter(
            status='finalizado',
            finalizado_em__year=now.year,
            finalizado_em__month=now.month
        )
        .aggregate(total=Sum('valor_servico'))
    )['total'] or 0

    faturamento_total = OrdemServico.objects.filter(
        status='finalizado'
    ).aggregate(
        total=Sum('valor_servico')
    )['total'] or 0

    faturamento_aberto = OrdemServico.objects.filter(
        status__in=['aberto', 'andamento']
    ).aggregate(
        total=Sum('valor_servico')
    )['total'] or 0
    
    # 🔥 NOVO — FATURAMENTO POR MÊS (últimos 12 meses)
    faturamento_por_mes = (
        OrdemServico.objects
        .filter(status='finalizado')
        .annotate(mes=TruncMonth('finalizado_em'))
        .values('mes')
        .annotate(total=Sum('valor_servico'))
        .order_by('mes')
    )

    # Formatar para enviar ao JS
    meses = []
    valores = []

    for item in faturamento_por_mes:
        meses.append(item['mes'].strftime('%b/%Y'))
        valores.append(float(item['total']))
    
    # PEÇAS
    
    valor_total_peca = ExpressionWrapper(
        F('valor_unitario') * F('quantidade'),
        output_field=DecimalField(max_digits=12, decimal_places=2)
    )
    pecas_mensal = (
        PecaOS.objects
        .filter(
            ordem_servico__status='finalizado',
            ordem_servico__finalizado_em__year=now.year,
            ordem_servico__finalizado_em__month=now.month
        )
        .aggregate(total=Sum(valor_total_peca))
    )['total'] or 0
    pecas_por_mes = (
        PecaOS.objects
        .filter(ordem_servico__status='finalizado')
        .annotate(mes=TruncMonth('ordem_servico__finalizado_em'))
        .values('mes')
        .annotate(total=Sum(valor_total_peca))
        .order_by('mes')
    )
    meses_pecas = []
    valores_pecas = []

    for item in pecas_por_mes:
        meses_pecas.append(item['mes'].strftime('%b/%Y'))
        valores_pecas.append(float(item['total']))

    return render(request, 'dashboard.html', {
        'abertas': OrdemServico.objects.filter(status='aberto').count(),
        'andamento': OrdemServico.objects.filter(status='andamento').count(),
        'finalizadas': OrdemServico.objects.filter(status='finalizado').count(),
        'finalizadas_hoje': OrdemServico.objects.filter(
            status=OrdemServico.Status.FINALIZADO,
            finalizado_em__date=date.today()
        ).count(),

        'faturamento_mensal': round(faturamento_mensal, 2),
        'faturamento_total': round(faturamento_total, 2),
        'faturamento_aberto': round(faturamento_aberto, 2),
        
        'meses': meses,
        'valores': valores,
        
        'pecas_mensal': round(pecas_mensal, 2),
        'meses_pecas': meses_pecas,
        'valores_pecas': valores_pecas,
    })
