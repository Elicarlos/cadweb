from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from . models import Categoria, Produto, Pedido, Cliente,  ItemPedido
from . forms import CategoriaForm, EstoqueForm, ItemPedidoForm, PagamentoForm, ProdutoForm, ClienteForm, PedidoForm
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps


def index(request):   
    return render(request,'index.html')

def dashboard(request):
    quant_produtos = Produto.objects.all().count()
    quant_clientes = Cliente.objects.all().count()
    contexto = {
        'quant_produtos': quant_produtos,
        'quant_clientes': quant_clientes
    }
    
    return render(request,'dashboard.html', contexto)

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id')        
    }
    
    return render(request, 'categoria/lista.html', contexto)

def cadastro_categoria(request):
    if request.method == "POST":
        form =  CategoriaForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Salvo com sucesso!')
            return redirect('categoria')
        
        else:
            messages.warning(request, 'Verifique os campos')
    
    else:
       form =  CategoriaForm() 
    
    
    return render (request, 'categoria/produtoForm.html', {'form': form})
      
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == "POST":
        form  = CategoriaForm(request.POST, instance=categoria)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com successo')
            return redirect('categoria')
            
        else:
            messages.warning(request, 'Vefique e dados e tente novamente')
            
    else:
        
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'categoria/editar.html', {'form': form})

def detalhes_categoria(request, id):
    
    categoria = get_object_or_404(Categoria, id=id)   
   
    context = {
        'categoria': categoria
    }
    return render(request, 'categoria/detalhes.html', context) 

def excluir_categoria(request, id):
    categoria  = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.success(request, 'Categoria deletada com sucesso!')
    return redirect('categoria')

def produtos(request):
    lista = Produto.objects.all().order_by('-id')
    return render(request, 'produto/lista.html', {'lista': lista})

def cadastro_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso')
            return redirect('produtos')
            
        else:
            messages.warning(request, 'Vefique os dados digitados')   
    else:
        form = ProdutoForm()
    
    return render(request, 'produto/form.html', {'form': form})
    
def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    
    return render(request, 'produto/detalhes.html', {'produto': produto})

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Atualizado com sucesso')
            return redirect('produtos')
        
        else:
            messages.warning(request, "Verifique os dados digitados")
            
    else:
        form = ProdutoForm(instance=produto)
            
    return render(request, 'produto/editar.html', {'form': form})

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id)
    produto.delete()
    messages.success(request, 'Produto deletado com sucesso')
    return redirect('produtos')

def clientes(request):
    lista = Cliente.objects.all().order_by('-id')
    return render(request, 'cliente/lista.html', {'lista': lista})

def cadastro_cliente(request):
    if request.method ==  "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente salvo com sucesso')
            return redirect('clientes')
        
        else:
            messages.warning(request, 'Verifique os dados e tente novamente')
            
    else:
        form = ClienteForm()
        
    return render(request, 'cliente/form.html', {'form': form})
    
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == "POST":
        form =  ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente atualizado com sucesso")
            return redirect('clientes')
        
        else:
            messages.error(request, "Verifique os dados e tente novamente")
            
    else:
        form = ClienteForm(instance=cliente)
        
    return render(request, 'cliente/editar.html', {'form': form})

def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'cliente/detalhes.html', {'cliente': cliente})

def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.warning(request, 'Cliente deletado com sucesso')
    return redirect('clientes')

def ajustar_estoque(reuquest, id):
    produto = Produto.objects.get(pk=id)
    estoque = produto.estoque
    
    if reuquest.method == 'POST':
        form = EstoqueForm(reuquest.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista = []
            lista.append(estoque.produto)
            return render(reuquest, 'produto/lista.html', {'lista': lista})      
        
    else:
        form = EstoqueForm(instance=estoque)
        
    return render(reuquest, 'produto/estoque.html', {'form': form}) 

def teste_01(request):
    return render(request, 'teste/teste01.html')

def teste_02(request):
    return render(request, 'teste/teste02.html')

def teste_03(request):
    return render(request, 'teste/teste03.html')

def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

def pedido(request):  
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})

def novo_pedido(request,id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)            
        except Cliente.DoesNotExist:            
            messages.error(request, 'Registro não encontrado')
            return redirect('cliente') 
        # cria um novo pedido com o cliente selecionado
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedido/form.html',{'form': form,})
    else:
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect(reverse('detalhes_pedido', args=[pedido.id]))


def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')  # Redireciona para a listagem    
    
    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else: # method Post
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False) # commit=False retorna o objeto item_pedido vindo do form para fazermos modificações adicionais antes de salvá-la, colocar o preço do produto, verificar estoque.
            item_pedido.preco = item_pedido.produto.preco # acessando o produto do relacionamento
            # realizar aqui o tratamento do estoque, para isso
            # Pegar o estoque (item_pedido.produto.estoque do relacionamento) atual 
            # verificar se a quantidade (item_pedido.produto.estoque.qtde) é suficiente para o item solicitado (tem_pedido.qtde)
            # Se não houver estoque suficiente, você pode adicionar uma mensagem de erro e não salvar a operação
            # Se sim, decrementar a quantidade do item no estoque do produto e salvar os objetos estoque e item_pedido
            item_pedido.save()
        else:
             messages.error(request, 'Erro ao adicionar produto')
                  
    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html',contexto )


def remover_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)
    
    pedido_id = item_pedido.pedido.id  # Armazena o ID do pedido antes de remover o item
    estoque = item_pedido.produto.estoque  # Obtém o estoque do produto
    estoque.qtde += item_pedido.qtde  # Devolve a quantidade do item ao estoque
    estoque.save()  # Salva as alterações no estoque
    # Remove o item do pedido
    item_pedido.delete()
    messages.success(request, 'Operação realizada com Sucesso')


    # Redireciona de volta para a página de detalhes do pedido
    return redirect('detalhes_pedido', id=pedido_id)

def form_pagamento(request,id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')  # Redireciona para a listagem    
    
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
    # prepara o formulário para um novo pagamento
    pagamento = Pagamento(pedido=pedido)
    form = PagamentoForm(instance=pagamento)
    contexto = {
        'pedido': pedido,
        'form': form,
    }    
    return render(request, 'pedido/pagamento.html',contexto)




