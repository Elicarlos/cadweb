from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo =  models.CharField(max_length=250)
    telefone = models.CharField(max_length=15, null=True)
    
    def __str__(self):
        return self.usuario.email
