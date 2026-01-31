from django import forms
from .models import OrdemServico, ComentarioOS, PecaOS


class OrdemServicoForm(forms.ModelForm):

    class Meta:
        model = OrdemServico
        fields = ['maquina', 'descricao_problema']
        
class OrdemServicoValorForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['valor_servico']

class ComentarioOSForm(forms.ModelForm):

    class Meta:
        model = ComentarioOS
        fields = ['comentario']
        
class PecaOSForm(forms.ModelForm):
    class Meta:
        model = PecaOS
        fields = ['nome', 'quantidade', 'valor_unitario', 'imagem']