from django.db import models
from django.db.models import Sum, F
from django.conf import settings
from maquinas.models import Maquina
from decimal import Decimal

# Create your models here.
class OrdemServico(models.Model):

    class Status(models.TextChoices):
        ABERTO = 'aberto', 'Aberto'
        EM_ANDAMENTO = 'andamento', 'Em andamento'
        FINALIZADO = 'finalizado', 'Finalizado'

    maquina = models.ForeignKey(
        Maquina,
        on_delete=models.CASCADE,
        related_name='ordens'
    )

    descricao_problema = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABERTO
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    finalizado_em = models.DateTimeField(null=True, blank=True)

    valor_servico = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )
    
    def total_pecas(self):
        return self.pecas.aggregate(
            total=Sum(F('valor_unitario') * F('quantidade'))
        )['total'] or 0

    def total_geral(self):
        return (self.valor_servico or 0) + self.total_pecas()

    def __str__(self):
        return f"OS #{self.id}"
    
class ComentarioOS(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    comentario = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário OS #{self.ordem_servico.id}"
    
class ImagemComentarioOS(models.Model):
    comentario = models.ForeignKey(
        ComentarioOS,
        on_delete=models.CASCADE,
        related_name='imagens'
    )
    imagem = models.ImageField(upload_to='os/comentarios/')
    enviada_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Imagem Comentário {self.comentario.id}"

    
class PecaOS(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='pecas'
    )
    nome = models.CharField(max_length=100)
    valor_unitario = models.DecimalField(max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"))
    quantidade = models.PositiveIntegerField(default=1)
    imagem = models.ImageField(upload_to='os/pecas/', null=True, blank=True)

    def total(self):
        return self.valor_unitario * self.quantidade

    def __str__(self):
        return f"{self.nome} (OS #{self.ordem_servico.id})"