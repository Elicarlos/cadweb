from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Create your models here.

class Cargo(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    permissoes = models.ManyToManyField(Permission, blank=True)
    
    def __str__(self):
        return self.nome

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo =  models.CharField(max_length=250)
    telefone = models.CharField(max_length=15, null=True)
    cargo =  models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.usuario.email
