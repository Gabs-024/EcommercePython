from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginated_by = '6'

class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produtos'
    slug_url_kwarg = 'slug'

class AdicionarAoCarrinho(View):
    ...

class RemoverDoCarrinho(View):
    ...

class Carrinho(View):
    ...

class Finalizar(View):
    ...