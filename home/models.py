import locale
from django.db import models
from django.conf import settings

class Base(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    
    class Meta:
        abstract = True



class Categoria(Base):
    nome = models.CharField(max_length=100)
    ordem =  models.IntegerField()
    
    def __str__(self):
        return self.nome
    
class Produto(Base):
    nome = models.CharField(max_length=250) 
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        self.nome
    
    
class Cliente(Base):
    nome = models.CharField(max_length=250)
    telefone = models.CharField(max_length=30)
    
class Pedido(Base):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.cliente}'
    
    

class ItemPedido(Base):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveBigIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    
    

