from django.contrib import admin
from . models import Categoria, Cliente, Produto, Estoque

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(Estoque)
