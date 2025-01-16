from django.shortcuts import render, redirect, get_object_or_404
from . models import Categoria, Produto, Pedido, Cliente,  ItemPedido
from . forms import CategoriaForm, EstoqueForm, ProdutoForm, ClienteForm
from django.contrib import messages


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

