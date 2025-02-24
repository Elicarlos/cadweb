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
    
    path('ajustar_estoque/<int:id>/', views.ajustar_estoque , name="ajustar_estoque"),
    
    path('teste01/', views.teste_01 , name="teste01"),
    path('teste02/', views.teste_02 , name="teste02"),
    path('teste03/', views.teste_03 , name="teste03"),
    
    path('buscar_dados/<str:app_modelo>/', views.buscar_dados , name="buscar_dados"),
    path('pedido/', views.pedido, name="pedido"),   
    path('pedido/<int:id>/', views.detalhes_pedido, name='detalhes_pedido'),   
    path('novo_pedido/<int:id>/', views.novo_pedido, name='novo_pedido'),
    path('remover_pedido/<int:id>/', views.remover_pedido, name='remover_pedido'),
    path('remover-item-pedido/<int:id>/', views.remover_item_pedido, name="remover_item_pedido"),
    path('editar-item-pedido/<int:id>/', views.editar_item_pedido, name="editar_item_pedido"),
    
    path('registrar_pagamento/<int:id>/', views.registrar_pagamento, name="registrar_pagamento"),
    path('nota-fiscal/<int:id>/', views.gerar_nota_fiscal, name="gerar_nota_fiscal"),
  

]