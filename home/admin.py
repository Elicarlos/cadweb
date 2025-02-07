from django.contrib import admin
from . models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido, Pagamento

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(Estoque)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Pagamento)
