from django.shortcuts import render, redirect, get_object_or_404
from . models import Categoria, Produto, Pedido, Cliente,  ItemPedido
from . forms import CategoriaForm, ProdutoForm
from django.contrib import messages



def index(request):
    return render(request,'index.html')


def categoria(request):
    # lista = [
    #     {
    #         'nome': 'Eltromestico',
    #         'ordem': 1
    #     },
    #     {
    #         'nome': 'Informática',
    #         'ordem': 1
    #     },
    #     {
    #         'nome': 'Móveis',
    #         'ordem': 1
    #     }
    # ]
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
    
    
    
    

