from django.contrib import admin
from . models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nome_completo', 'telefone')
    search_fields = ('usuario__email', 'nome_completo', 'telefone')