from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from . models import Categoria, Estoque, Pagamento, Produto, Pedido, Cliente,  ItemPedido
from . forms import CategoriaForm, EstoqueForm, ItemPedidoForm, PagamentoForm, ProdutoForm, ClienteForm, PedidoForm
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import Pedido


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

def remover_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
   
    itens_pedido = ItemPedido.objects.filter(pedido=pedido)
    if itens_pedido.exists():        
        for item in itens_pedido:
            estoque = Estoque.objects.get(produto=item.produto)
            estoque.qtde += item.qtde
            estoque.save()

       
        itens_pedido.delete()

    
    pagamentos = Pagamento.objects.filter(pedido=pedido)
    if pagamentos.exists():
        messages.error(request, "Não é possível excluir um pedido com pagamentos associados!")
        return redirect('detalhes_pedido', id=id)      
    pedido.delete()
    messages.success(request, "Pedido removido com sucesso!")

    return redirect('pedido') 

def novo_pedido(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = cliente
            pedido.status = Pedido.NOVO  # Garante que sempre inicia como "Novo"
            pedido.save()
            messages.success(request, "Pedido criado com sucesso! Adicione produtos agora.")
            return redirect('detalhes_pedido', id=pedido.id)
    else:
        pedido = Pedido(cliente=cliente, status=Pedido.NOVO)  # Criando um pedido sem salvar
        form = PedidoForm(instance=pedido)

    return render(request, 'pedido/form.html', {'form': form, 'cliente': cliente})

def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            item_pedido.pedido = pedido  # Associa ao pedido correto
            item_pedido.preco = item_pedido.produto.preco  # Define o preço do produto
            
            # Verifica se há estoque suficiente
            if item_pedido.atualizar_estoque():
                item_pedido.save()
                messages.success(request, 'Produto adicionado com sucesso!')
            else:
                messages.error(request, "Estoque insuficiente!")

            return redirect('detalhes_pedido', id=pedido.id)
        else:
            messages.error(request, 'Erro ao adicionar produto')

    else:
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)

    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html', contexto)



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
    messages.success(request, 'Item removido com sucesso')


    # Redireciona de volta para a página de detalhes do pedido
    return redirect('detalhes_pedido', id=pedido_id)

def editar_item_pedido(request, id):
    item_pedido = get_object_or_404(ItemPedido, id=id)
    pedido_id = item_pedido.pedido.id

    if request.method == "POST":
        form = ItemPedidoForm(request.POST, instance=item_pedido)

        if form.is_valid():
            nova_qtde = form.cleaned_data.get("qtde")  # Obtendo nova quantidade do formulário
            estoque = Estoque.objects.get(produto=item_pedido.produto)  # Buscando o estoque do produto
            
            diferenca_qtde = nova_qtde - item_pedido.qtde  # Calculando a diferença de quantidade

            if diferenca_qtde > 0 and estoque.qtde < diferenca_qtde:
                messages.error(request, f"Estoque insuficiente! Apenas {estoque.qtde} disponíveis.")
            else:
                # Atualiza o estoque apenas se a quantidade for alterada
                estoque.qtde -= diferenca_qtde
                estoque.save()

                item_pedido.qtde = nova_qtde
                item_pedido.save()
                messages.success(request, "Item atualizado com sucesso!")
                return redirect('detalhes_pedido', id=pedido_id)
    
    else:
        form = ItemPedidoForm(instance=item_pedido)

    return render(request, 'itemPedido/editar.html', {'form': form})
   
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

def registrar_pagamento(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == "POST":
        form = PagamentoForm(request.POST)

        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.pedido = pedido  

            
            total_devido = pedido.total - pedido.total_pago
            if pagamento.valor > total_devido:
                messages.error(request, f"O valor do pagamento ({pagamento.valor}) excede o total devido ({total_devido}).")
                return redirect('registrar_pagamento', id=id)  

            pagamento.save()  
            messages.success(request, "Pagamento registrado com sucesso!")

           
            if pedido.total_pago >= pedido.total:
                pedido.status = Pedido.CONCLUIDO
                pedido.save()

            return redirect('detalhes_pedido', id=id)  

    else:
        
        pagamento = Pagamento(pedido=pedido)
        form = PagamentoForm(instance=pagamento)

    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/pagamento.html', contexto)  





def gerar_nota_fiscal(request, id):
    pedido = Pedido.objects.get(pk=id)

    # Configuração do PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="nota_fiscal_pedido_{pedido.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, altura - 50, "NOTA FISCAL")

    # Dados do Pedido
    p.setFont("Helvetica", 12)
    data_pedido_str = pedido.data_pedidof  # Usa a nova propriedade corrigida

    
    p.drawString(50, altura - 100, f"Pedido ID: {pedido.id}")
    p.drawString(50, altura - 120, f"Cliente: {pedido.cliente.nome}")
    p.drawString(50, altura - 140, f"Data do Pedido: {data_pedido_str}")
    p.drawString(50, altura - 160, f"Status: {pedido.get_status_display()}")

    # Linha Separadora
    p.line(50, altura - 180, largura - 50, altura - 180)

    # Cabeçalho da Tabela
    y = altura - 200
    p.drawString(50, y, "Produto")
    p.drawString(300, y, "Quantidade")
    p.drawString(400, y, "Preço Unitário (R$)")
    p.drawString(500, y, "Subtotal (R$)")
    
    y -= 20  # Espaço abaixo do cabeçalho

    # Itens do Pedido
    for item in pedido.itempedido_set.all():
        p.drawString(50, y, item.produto.nome)
        p.drawString(300, y, str(item.qtde))
        p.drawString(400, y, f"R$ {item.preco:.2f}")
        p.drawString(500, y, f"R$ {item.subtotal:.2f}")
        y -= 20  # Move para a próxima linha

    # Linha Final Separadora
    p.line(50, y, largura - 50, y)
    y -= 20

    # Total do Pedido
    p.setFont("Helvetica-Bold", 12)
    p.drawString(400, y, "Total do Pedido:")
    p.drawString(500, y, f"R$ {pedido.total:.2f}")

    p.showPage()
    p.save()
    return response



