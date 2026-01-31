from django.utils import timezone
from .models import OrdemServico

def iniciar_os(ordem: OrdemServico):
    if ordem.status != OrdemServico.Status.ABERTO:
        raise ValueError("A ordem não está em aberto")

    ordem.status = OrdemServico.Status.EM_ANDAMENTO
    ordem.save()

def finalizar_os(ordem: OrdemServico):
    if ordem.status == OrdemServico.Status.FINALIZADO:
        raise ValueError("A ordem já foi finalizada")

    ordem.status = OrdemServico.Status.FINALIZADO
    ordem.finalizado_em = timezone.now()
    ordem.save()