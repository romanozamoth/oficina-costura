from django.db import models
from clientes.models import Cliente

class Maquina(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='maquinas'
    )

    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, blank=True)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='maquinas/', null=True, blank=True)

    def __str__(self):
        return f"{self.modelo} - {self.cliente.nome} - {self.cliente.telefone_formatado()}"
