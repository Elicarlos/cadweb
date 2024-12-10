from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Usuario


@receiver(post_save, sender=User)
def criar_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(usuario=instance)