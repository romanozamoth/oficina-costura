from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Cliente
from .forms import ClienteForm

# Create your views here.
def listar_clientes(request):
    clientes = Cliente.objects.all()

    cliente_id = request.GET.get("cliente")
    if cliente_id:
        clientes = clientes.filter(id=cliente_id)

    return render(
        request,
        'clientes/list.html',
        {'clientes': clientes}
    )

def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_listar')
    else:
        form = ClienteForm()

    return render(
        request,
        'clientes/form.html',
        {'form': form}
    )

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes_listar')
    else:
        form = ClienteForm(instance=cliente)

    return render(
        request,
        'clientes/form.html',
        {'form': form}
    )

def remover_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes_listar')

    return render(
        request,
        'clientes/delete.html',
        {'cliente': cliente}
    )

def clientes_autocomplete(request):
    term = request.GET.get("q", "")

    clientes = Cliente.objects.filter(
        Q(nome__icontains=term) |
        Q(telefone__icontains=term)
    ).order_by("nome")[:10]

    data = [
        {
            "id": c.id,
            "text": f"{c.nome} - {c.telefone_formatado()}"
        }
        for c in clientes
    ]

    return JsonResponse(data, safe=False)