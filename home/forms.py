from datetime import date
from . models import Categoria, Cliente, Estoque, Produto
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
   
    
    preco = forms.DecimalField(
        label="Preco",
        decimal_places=2,
        max_digits=10,
        widget=forms.TextInput(attrs={
            'class': 'money form-control',
            'maxlength': 500,
            'placeholder': '0,000,00'})
        
    )
   
    
    img_base64 = forms.HiddenInput()
        
    
    class Meta:
        model = Produto
        fields = '__all__'
        exclude = ['criado_por']
        widgets = {
            'categoria': forms.HiddenInput()
        }
        
    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True
        
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
    
    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc > date.today():
            raise forms.ValidationError("A data de nascimento não pode estar no futuro.")
        return datanasc
    
    class Meta:
        model = Cliente
        
        fields = '__all__'
        exclude = ['criado_por']
        
        
class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'qtde']
        
        widgets = {
            'produto': forms.HiddenInput(),
            'qtde': forms.TextInput(attrs={'class': 'inteiro form-control',}),
        }
        
    
        
    
    