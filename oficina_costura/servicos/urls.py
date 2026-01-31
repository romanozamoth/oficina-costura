from django.urls import path
from . import views

urlpatterns = [
    path('', views.kanban_servicos, name='servicos_kanban'),
    path('nova/', views.criar_os, name='servicos_criar'),
    path('<int:os_id>/', views.servicos_detalhe, name='servicos_detalhe'),

    path('<int:os_id>/iniciar/', views.iniciar_ordem, name='servicos_iniciar'),
    path('<int:os_id>/finalizar/', views.finalizar_ordem, name='servicos_finalizar'),
    path('servicos/<int:os_id>/excluir/', views.servicos_excluir, name='servicos_excluir'),
    
    path('<int:os_id>/pecas/nova/', views.adicionar_peca_os, name='adicionar_peca_os'),
    path('pecas/<int:peca_id>/editar/', views.editar_peca_os, name='editar_peca_os'),
    path('pecas/<int:peca_id>/excluir/', views.excluir_peca_os, name='excluir_peca_os'),
    
    path('comentarios/<int:id>/editar/', views.editar_comentario, name='editar_comentario'),
    path('comentarios/<int:id>/excluir/', views.excluir_comentario, name='excluir_comentario'),
    path('comentarios/imagem/<int:id>/excluir/', views.excluir_imagem, name='excluir_imagem'),

    path('autocomplete/kanban/', views.autocomplete_kanban, name='autocomplete_kanban'),
]
