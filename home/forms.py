from . models import Categoria, Cliente, Produto
from django import forms

class CategoriaForm(forms.ModelForm):
    nome = forms.CharField(
        label="Nome",
        max_length=250,
        widget=forms.TextInput(attrs={"class": "form-control",
                                      "id": "id_nome" ,
                                      })
    )
    ordem = forms.DecimalField(
        label="Ordem",
        max_digits=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id':'id_ordem'})
    )    
    class Meta:
        model = Categoria
        
        fields = '__all__'
        
        exclude = ['criado_por']
        
class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(
        label="Nome",
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nome'})
    )
    categoria = forms.ModelChoiceField(
        label='Categoria',
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    preco = forms.DecimalField(
        label="Preco",
        decimal_places=2,
        max_digits=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preco'})
        
    )
    estoque = forms.IntegerField(
        label="Estoque",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'estoque'})
    )
    
    class Meta:
        model = Produto
        fields = '__all__'
        exclude = ['criado_por']
        
class ClienteForm(forms.ModelForm):
    nome = forms.CharField(
        label="Nome",
        widget=forms.TextInput(attrs={'class': 'form-control'})
        
    )
    
    cpf = forms.CharField(
        label="CPF",
        widget=forms.TextInput(attrs={'class': 'cpf form-control'})
    )
    
    telefone = forms.CharField(
        label="Telefone",
        widget=forms.TextInput(attrs={'class':'telefone form-control'})
    )
    
    datanasc = forms.DateField(
        label="Data Nascimento",
        widget=forms.DateInput(attrs={'class': ' data form-control', }, format="%d/%m%Y")
    )
    
    class Meta:
        model = Cliente
        
        fields = '__all__'
        exclude = ['criado_por']
    
    