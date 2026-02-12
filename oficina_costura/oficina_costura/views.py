from django.shortcuts import render
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import date
from servicos.models import OrdemServico
from django.db.models import Sum

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
    })
