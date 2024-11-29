from django.shortcuts import render
from . models import Categoria



def index(request):
    return render(request,'index.html')


def categoria(request):
    lista = [
        {
            'nome': 'Eltromestico',
            'ordem': 1
        },
        {
            'nome': 'Informática',
            'ordem': 1
        },
        {
            'nome': 'Móveis',
            'ordem': 1
        }
    ]
    contexto = {
        # 'lista': Categoria.objects.all().order_by('id')
        'lista': lista
    }
    
    return render(request, 'categoria/lista.html', contexto)

