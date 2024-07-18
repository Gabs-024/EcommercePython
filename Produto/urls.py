from django.urls import path
from .views import (
    ListaProdutos, DetalheProduto, AdicionarAoCarrinho, 
    RemoverDoCarrinho, Carrinho, ResumoPedido, Busca
)

app_name = 'produto'

urlpatterns = [
    path('', ListaProdutos.as_view(), name="lista" ),
    path('adicionaraocarrinho/', AdicionarAoCarrinho.as_view(), 
        name="adicionaraocarrinho" ),
    path('removerdocarrinho/', RemoverDoCarrinho.as_view(), 
        name="removerdocarrinho" ),
    path('carrinho/', Carrinho.as_view(), name="carrinho" ),
    path('resumopedido/', ResumoPedido.as_view(), name="resumopedido" ),
    path('busca/', Busca.as_view(), name="busca" ),
    path('<slug:slug>/', DetalheProduto.as_view(), name="detalhe" ),
]
