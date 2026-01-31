from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import ComentarioOS, OrdemServico, PecaOS, ImagemComentarioOS
from .forms import OrdemServicoForm, ComentarioOSForm, OrdemServicoValorForm, PecaOSForm
from .services import iniciar_os, finalizar_os

def kanban_servicos(request):
    q = request.GET.get('q', '').strip()

    filtro = Q()

    if q:
        filtro = (
            Q(maquina__modelo__icontains=q) |
            Q(maquina__cliente__nome__icontains=q) |
            Q(maquina__cliente__telefone__icontains=q)
        )

    abertos = OrdemServico.objects.filter(
        status=OrdemServico.Status.ABERTO
    ).filter(filtro).select_related('maquina__cliente')

    andamento = OrdemServico.objects.filter(
        status=OrdemServico.Status.EM_ANDAMENTO
    ).filter(filtro).select_related('maquina__cliente')

    finalizados = OrdemServico.objects.filter(
        status=OrdemServico.Status.FINALIZADO
    ).filter(filtro).select_related('maquina__cliente')

    return render(request, 'servicos/kanban.html', {
        'abertos': abertos,
        'andamento': andamento,
        'finalizados': finalizados,
        'q': q,
    })

def criar_os(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicos_kanban')
    else:
        form = OrdemServicoForm()

    return render(request, 'servicos/form.html', {'form': form})

def servicos_detalhe(request, os_id):
    os = get_object_or_404(OrdemServico, id=os_id)

    comentario_form = ComentarioOSForm()
    valor_form = OrdemServicoValorForm(instance=os)

    if request.method == 'POST':
        # 🔹 Salvar comentário
        if 'salvar_comentario' in request.POST:
            comentario_form = ComentarioOSForm(request.POST)
            imagens = request.FILES.getlist('imagens')
            
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.ordem_servico = os
                comentario.save()
                
                # 🔹 Salvar imagens do comentário
                for img in imagens:
                    ImagemComentarioOS.objects.create(
                        comentario=comentario,
                        imagem=img
                    )
                    
                return redirect('servicos_detalhe', os_id=os.id)

        # 🔹 Salvar valor
        elif 'salvar_valor' in request.POST:
            valor_form = OrdemServicoValorForm(request.POST, instance=os)
            if valor_form.is_valid():
                valor_form.save()
                return redirect('servicos_detalhe', os_id=os.id)

    return render(request, 'servicos/detalhe.html', {
        'os': os,
        'comentario_form': comentario_form,
        'valor_form': valor_form
    })

def iniciar_ordem(request, os_id):
    ordem = get_object_or_404(OrdemServico, id=os_id)
    iniciar_os(ordem)
    return redirect('servicos_kanban')

def finalizar_ordem(request, os_id):
    ordem = get_object_or_404(OrdemServico, id=os_id)
    finalizar_os(ordem)
    return redirect('servicos_kanban')

def servicos_excluir(request, os_id):
    os = get_object_or_404(OrdemServico, id=os_id)

    if request.method == 'POST':
        os.delete()
        return redirect('servicos_kanban')

    return render(request, 'servicos/delete.html', {'os': os})

def adicionar_peca_os(request, os_id):
    os = get_object_or_404(OrdemServico, id=os_id)

    if request.method == 'POST':
        form = PecaOSForm(request.POST, request.FILES)  # ⚠️ request.FILES necessário
        if form.is_valid():
            peca = form.save(commit=False)
            peca.ordem_servico = os
            peca.save()
            return redirect('servicos_detalhe', os.id)
    else:
        form = PecaOSForm()

    return render(request, 'servicos/peca_form.html', {'form': form, 'os': os})

def editar_peca_os(request, peca_id):
    peca = get_object_or_404(PecaOS, id=peca_id)

    if request.method == 'POST':
        form = PecaOSForm(request.POST, request.FILES, instance=peca)  # ⚠️ request.FILES necessário
        if form.is_valid():
            form.save()
            return redirect('servicos_detalhe', peca.ordem_servico.id)
    else:
        form = PecaOSForm(instance=peca)

    return render(request, 'servicos/peca_form.html', {'form': form, 'os': peca.ordem_servico})

def excluir_peca_os(request, peca_id):
    peca = get_object_or_404(PecaOS, id=peca_id)
    os_id = peca.ordem_servico.id
    peca.delete()
    return redirect('servicos_detalhe', os_id)

def editar_comentario(request, id):
    comentario = get_object_or_404(ComentarioOS, id=id)

    if request.method == 'POST':
        form = ComentarioOSForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            
            # Aqui podemos processar imagens novas, se vierem pelo upload
            imagens_novas = request.FILES.getlist('imagens')
            for img in imagens_novas:
                ImagemComentarioOS.objects.create(comentario=comentario, imagem=img)
            
            return redirect('servicos_detalhe', comentario.ordem_servico.id)
    else:
        form = ComentarioOSForm(instance=comentario)

    imagens = comentario.imagens.all()  # Todas as imagens atuais do comentário

    return render(request, 'servicos/comentario_form.html', {
        'form': form,
        'comentario': comentario,
        'imagens': imagens,
    })

def excluir_comentario(request, id):
    comentario = get_object_or_404(ComentarioOS, id=id)
    os_id = comentario.ordem_servico.id

    # Apaga arquivos físicos das imagens
    for img in comentario.imagens.all():
        img.imagem.delete()

    comentario.delete()
    return redirect('servicos_detalhe', os_id)

def excluir_imagem(request, id):
    imagem = get_object_or_404(ImagemComentarioOS, id=id)
    os_id = imagem.comentario.ordem_servico.id
    imagem.imagem.delete()
    imagem.delete()
    return redirect('servicos_detalhe', os_id)

def autocomplete_kanban(request):
    term = request.GET.get('term', '').strip()

    if len(term) < 2:
        return JsonResponse([], safe=False)

    ordens = (
        OrdemServico.objects
        .filter(
            Q(maquina__modelo__icontains=term) |
            Q(maquina__cliente__nome__icontains=term) |
            Q(maquina__cliente__telefone__icontains=term)
        )
        .select_related('maquina__cliente')
        .distinct()[:10]
    )

    data = [
        {
            "label": f"{os.maquina.modelo} — {os.maquina.cliente.nome}",
            "value": f"{os.maquina.cliente.nome}"
        }
        for os in ordens
    ]

    return JsonResponse(data, safe=False)