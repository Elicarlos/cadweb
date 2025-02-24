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
    img_base64 = models.TextField(blank=True)
    
    @property
    def estoque(self):
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item
        
    
    def __str__(self):
        return self.nome
        
class Estoque(Base):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    qtde = models.IntegerField()
    
    def __str__(self):
        return f'{self.produto} - quantidade: {self.qtde}'
    
    
class Cliente(Base):
    nome = models.CharField(max_length=250)
    telefone = models.CharField(max_length=30)
    cpf = models.CharField(max_length=20, unique=True)
    datanasc = models.DateField(verbose_name="Data de nascimento", default="2024/11/03", null=True, blank=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
    
    @property
    def datanascimento(self):
        if self.datanasc:
            return self.datanasc.strftime("%d/%m/%Y")
        return None
    
class Pedido(Base):
    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4
    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em andamento'),
        (CONCLUIDO, 'Concluido'),
        (CANCELADO, 'Cancelado')
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    
    
    def __str__(self):
        return f'{self.cliente}'
    
    @property
    def data_pedidof(self): 
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return "Data não disponível"

    
    @property
    def total(self):
        """Calcula o total de todos os itens no pedido, formatado como moeda local"""
        total = sum(item.qtde * item.preco for item in self.itempedido_set.all())
        return total
    
    @property
    def qtdeItens(self):
        """Conta a qtde de itens no pedido, """
        return self.itempedido_set.count()
    
    # lista de todos os pagamentos realiados
    @property
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self)    
    
    #Calcula o total de todos os pagamentos do pedido
    @property
    def total_pago(self):
        """Soma o total pago"""
        total = sum(pagamento.valor for pagamento in self.pagamentos.all())
        return total or 0
    
    
    @property
    def status_display(self):
        """Define o status corretamente baseado no pagamento"""
        if self.total_pago >= self.total and self.total > 0:
            return "Pago"
        return self.get_status_display()

   
    
    @property
    def debito(self):
        return "implementar"
    
    @property
    def produtos_lista(self):
        produtos = self.itempedido_set.all()[:3]
        nomes_produtos = [item.produto.nome for item in produtos]
        return ", ".join(nomes_produtos)


    

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.produto.nome } (Qtd: {self.qtde} - Preço Unitário: {self.preco })'
    
    @property
    def subtotal(self):
        return self.qtde * self.preco
    
    def verificar_estoque(self):
        if self.produto.estoque.qtde < self.qtde:
            return False
        
        return True
    
    def atualizar_estoque(self):
        """Decrementa a quantidade do estoque ao salvar um novo item do pedido."""
        estoque = Estoque.objects.filter(produto=self.produto).first()
        if estoque and self.verificar_estoque():
            estoque.qtde -= self.qtde
            estoque.save()  # Importante! Salva a alteração no banco de dados
            return True
        return False
    
class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4
    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]


    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)
    
    @property
    def data_pgtof(self):
        """Retorna a data no formato DD/MM/AAAA HH:MM"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None

    
    
    
    
    


    
    
    

