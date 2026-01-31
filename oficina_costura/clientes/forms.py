import re
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    telefone = forms.CharField(
        max_length=15,  # aceita máscara
        label="Telefone",
        widget=forms.TextInput(attrs={
            'id': 'telefone',
            'placeholder': '(11) 91234-5678',
            'inputmode': 'numeric',
            'autocomplete': 'off'
        })
    )
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'telefone': forms.TextInput(attrs={
                'id': 'telefone',
                'placeholder': '(11) 91234-5678',
                'inputmode': 'numeric',
                'autocomplete': 'off'
            }),
            'endereco': forms.Textarea(attrs={'rows': 3}),
        }
        
    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone", "")
        telefone = re.sub(r"\D", "", telefone)

        if len(telefone) != 11:
            raise forms.ValidationError("Informe um celular válido com DDD.")

        return telefone