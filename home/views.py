from django.shortcuts import render, redirect
from . models import Categoria
from . forms import CategoriaForm
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
        'lista': Categoria.objects.all().order_by('id')
        
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
    categoria = Categoria.objects.filter(id=id)
    form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/edite.html', {'form': form}) 
    
    
    

