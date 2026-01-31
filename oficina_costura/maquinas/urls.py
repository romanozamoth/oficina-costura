from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_maquinas, name='maquinas_listar'),
    path('novo/', views.criar_maquina, name='maquinas_criar'),
    path('<int:maquina_id>/editar/', views.editar_maquina, name='maquinas_editar'),
    path('<int:maquina_id>/remover/', views.remover_maquina, name='maquinas_remover'),
    path('api/autocomplete/', views.maquinas_autocomplete, name='maquinas_autocomplete'),
]
