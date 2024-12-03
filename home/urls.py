from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoria/', views.categoria, name='categoria'),
    path('cadastro-categoria/', views.cadastro_categoria, name='cadastro-categoria'),
    path('editar-categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('detalhes-categoria/<int:id>/', views.detalhes_categoria, name='detalhes_categoria'),
    path('excluir-categoria/<int:id>/', views.excluir_categoria, name='excluir_categoria')
]