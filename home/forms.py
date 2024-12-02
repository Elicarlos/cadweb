from . models import Categoria
from django import forms

class CategoriaForm(forms.ModelForm):
    nome = forms.CharField(
        label="Nome",
        max_length=250,
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Categoria...'})
    )
    ordem = forms.DecimalField(
        label="Ordem",
        max_digits=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ordem'})
    )
    

    
    class Meta:
        model = Categoria
        
        fields = '__all__'