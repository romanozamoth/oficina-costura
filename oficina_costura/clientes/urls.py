from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_clientes, name='clientes_listar'),
    path('novo/', views.criar_cliente, name='clientes_criar'),
    path('<int:cliente_id>/editar/', views.editar_cliente, name='clientes_editar'),
    path('<int:cliente_id>/remover/', views.remover_cliente, name='clientes_remover'),
    path('api/autocomplete/', views.clientes_autocomplete, name='clientes_autocomplete'),
]
