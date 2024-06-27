from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib import messages

from ..Produto.models import Variacao
from ..utils import utils
from .models import Pedido, ItemPedido

class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        return super().dispatch(*args, **kwargs)
    
class Pagar(DispatchLoginRequired, DetailView):
        template_name = 'pedido/pagar.html'
        model = Pedido
        pk_url_kwarg = 'pk'
        context_object_name = 'pedido'

        def get_queryset(self, *args, **kwargs):
            qs = super().get_queryset(*args, **kwargs)
            qs = qs.filter(usuario=self.request.user)
            return qs

class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa efetuar o login.'
            )
            return redirect('perfil:criar')
        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:lista')
        
        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_id = [v for v in carrinho]
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id_in=carrinho_variacao_id)
        )

        for variacao in bd_variacoes:
            vid = variacao.id

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unit = carrinho[vid]['preco_unitario']
            preco_unit_promo = carrinho[vid]['preco_unitario_promocional']

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unit
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * \
                    preco_unit_promo
                error_msg_estoque = 'Estoque insuficiente para alguns itens no seu carrinho.'\
                                    'Por favor, verifique quais produtos foram afetados a seguir.'
                if error_msg_estoque:
                    messages.error(
                        self.request,
                        error_msg_estoque
                )
                self.request.session.save()
                return redirect('produto:carrinho')
            
        qtd_total_carrinho = utils.total_carrinho(carrinho)
        valor_total_carrinho = utils.valor_total_carrinho(carrinho)

        pedido = Pedido(
            usuario = self.request.user,
            total = valor_total_carrinho,
            qtd_carrinho = qtd_total_carrinho,
            status='C',
        )
        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido = pedido,
                    produto = v['produto_nome'],
                    produto_id = v['produto_id'],
                    variacao = v['variacao_nome'],
                    variacao_id = v['variacao_id'],
                    preco = v['preco_quantitativo']
                    preco_promocional = v['preco_quantitativo_promocional']
                    quantidade = v['quantidade']
                    imagem = v['imagem']
                ) for v in carrinho.values()
            ]
        )

        del self.request.session['carrinho']
        # return render  (self.request, self.template_name, contexto)
        return redirect('pedido:lista')

class Lista(View):
    ...

class Detalhe(View):
    ...