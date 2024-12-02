from django.shortcuts import render, redirect
from . models import Categoria
from . forms import CategoriaForm



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
            
            return redirect('categoria')
    
    else:
       form =  CategoriaForm() 
    
    
    return render (request, 'categoria/produtoForm.html', {'form': form})
    
    
        
    
    
    
    
    

