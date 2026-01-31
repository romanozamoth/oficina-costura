from django.shortcuts import render
from django.utils import timezone
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

    return render(request, 'dashboard.html', {
        'abertas': OrdemServico.objects.filter(status='aberto').count(),
        'andamento': OrdemServico.objects.filter(status='andamento').count(),
        'finalizadas': OrdemServico.objects.filter(status='finalizado').count(),
        'finalizadas_hoje': OrdemServico.objects.filter(
            status=OrdemServico.Status.FINALIZADO,
            finalizado_em__date=date.today()
        ).count(),

        'faturamento_mensal': faturamento_mensal,
        'faturamento_total': faturamento_total,
        'faturamento_aberto': faturamento_aberto
    })
