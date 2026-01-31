from django import forms
from .models import Maquina

class MaquinaForm(forms.ModelForm):

    class Meta:
        model = Maquina
        fields = ['cliente', 'modelo', 'numero_serie', 'descricao', 'imagem']
        widgets = {
            'modelo': forms.TextInput(attrs={'placeholder': 'Modelo da máquina'}),
            'numero_serie': forms.TextInput(attrs={'placeholder': 'Número de série'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
