def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.',',')

def total_carrinho(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def valor_total_carrinho(carrinho):
    return sum (
        {
        item.get('preco_quantitativo_promocional')
        if item.get('preco_quantitativo_promocional')
        else item.get('preco_quantitativo')
        in carrinho.values()
        }
    )