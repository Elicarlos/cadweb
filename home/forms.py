from datetime import date
from . models import Categoria, Cliente, Estoque, ItemPedido, Produto, Pedido, Pagamento
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
        
class PedidoForm(forms.ModelForm):    
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.HiddenInput()
        }
            
class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido','produto', 'qtde']
        
        def clean(self):
            cleaned_data = super().clean()
            produto = cleaned_data.get('produto')
            qtde = cleaned_data.get('qtde')
            
            
            if produto and qtde:
                if produto.estoque.qtde < qtde:
                    raise forms.ValidationError(f'Estoque insuficiente! Apenas { produto.estoque.qtde} disponivel')
            
            return cleaned_data


        widgets = {
            'pedido': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'produto': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'qtde':forms.TextInput(attrs={'class': 'form-control',}),
        }


from django import forms
from .models import Pagamento

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['pedido', 'forma', 'valor']
        widgets = {
            'pedido': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'forma': forms.Select(attrs={'class': 'form-control'}),  # Select para escolha da forma de pagamento
            'valor': forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
        }

    def __init__(self, *args, **kwargs):
        # Pegando o pedido do contexto
        self.pedido = kwargs.pop('pedido', None)
        super(PagamentoForm, self).__init__(*args, **kwargs)
        self.fields['valor'].localize = True
        self.fields['valor'].widget.is_localized = True    

    def clean_valor(self):
        """
        Valida se o valor inserido não excede o valor restante do pedido.
        """
        valor = self.cleaned_data.get('valor')

        if self.pedido:
            total_devido = self.pedido.total - self.pedido.total_pago
            if valor > total_devido:
                raise forms.ValidationError(
                    f"O valor do pagamento ({valor}) excede o total devido ({total_devido})."
                )
        
        if valor <= 0:
            raise forms.ValidationError("O valor do pagamento deve ser maior que zero.")

        return valor

    