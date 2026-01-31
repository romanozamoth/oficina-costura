from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Maquina
from .forms import MaquinaForm

def listar_maquinas(request):
    maquinas = Maquina.objects.select_related("cliente")

    cliente_id = request.GET.get("cliente")
    maquina_id = request.GET.get("maquina")

    if cliente_id:
        maquinas = maquinas.filter(cliente_id=cliente_id)

    if maquina_id:
        maquinas = maquinas.filter(id=maquina_id)

    return render(
        request,
        'maquinas/list.html',
        {'maquinas': maquinas}
    )
def criar_maquina(request):
    if request.method == 'POST':
        form = MaquinaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('maquinas_listar')
    else:
        form = MaquinaForm()

    return render(
        request,
        'maquinas/form.html',
        {'form': form}
    )
def editar_maquina(request, maquina_id):
    maquina = get_object_or_404(Maquina, id=maquina_id)

    if request.method == 'POST':
        form = MaquinaForm(request.POST, request.FILES, instance=maquina)
        if form.is_valid():
            form.save()
            return redirect('maquinas_listar')
    else:
        form = MaquinaForm(instance=maquina)

    return render(
        request,
        'maquinas/form.html',
        {'form': form}
    )
def remover_maquina(request, maquina_id):
    maquina = get_object_or_404(Maquina, id=maquina_id)

    if request.method == 'POST':
        maquina.delete()
        return redirect('maquinas_listar')

    return render(
        request,
        'maquinas/delete.html',
        {'maquina': maquina}
    )

def maquinas_autocomplete(request):
    term = request.GET.get("q", "")

    maquinas = Maquina.objects.select_related("cliente").filter(
        Q(modelo__icontains=term) |
        Q(numero_serie__icontains=term)
    )[:10]

    data = [
        {
            "id": m.id,
            "text": f"{m.modelo} — {m.cliente.nome}"
        }
        for m in maquinas
    ]

    return JsonResponse(data, safe=False)