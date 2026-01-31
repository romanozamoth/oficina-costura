from django.db import models
import re

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def telefone_formatado(self):
        if len(self.telefone) == 11:
            return f"({self.telefone[:2]}) {self.telefone[2:7]}-{self.telefone[7:]}"
        elif len(self.telefone) == 10:
            return f"({self.telefone[:2]}) {self.telefone[2:6]}-{self.telefone[6:]}"
        return self.telefone

    def telefone_whatsapp(self):
        return f"https://wa.me/55{self.telefone}"

    def __str__(self):
        return f"{self.nome} - {self.telefone_formatado()}"