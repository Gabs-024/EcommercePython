def formata_preco(val):
    valor = float(val)
    return f'R$ {valor:.2f}'.replace('.',',')

def total_carrinho(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def valor_total_carrinho(carrinho):
    return sum(
        item.get('preco_quantitativo_promocional', item.get('preco_quantitativo'))
        for item in carrinho.values()
    )