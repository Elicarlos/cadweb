from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="index"),
    path('categoria/', views.categoria, name='categoria'),
    path('cadastro-categoria/', views.cadastro_categoria, name='cadastro-categoria'),
    path('editar-categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('detalhes-categoria/<int:id>/', views.detalhes_categoria, name='detalhes_categoria'),
    path('excluir-categoria/<int:id>/', views.excluir_categoria, name='excluir_categoria'),
    
    path('produtos/', views.produtos, name="produtos"),
    path("cadastro-produto/", views.cadastro_produto, name="cadastro-produto"),
    path('detalhes_produto/<int:id>/', views.detalhes_produto, name='detalhes_produto'),
    path('editar_produto/<int:id>/', views.editar_produto, name="editar_produto"),
    path('excluir_produto/<int:id>/', views.excluir_produto , name="excluir_produto"),
    
    path('clientes/', views.clientes, name="clientes"),
    path("cadastro-cliente/", views.cadastro_cliente, name="cadastro-cliente"),
    path('detalhes_cliente/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('excluir_cliente/<int:id>/', views.excluir_cliente , name="excluir_cliente"),
    
    path('ajustar_estoque/<int:id>/', views.ajustar_estoque , name="ajustar_estoque")
    
    
    
]