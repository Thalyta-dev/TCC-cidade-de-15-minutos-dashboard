class AmenidadeUtil:
    
    def titulo_amenidade_mais_comum(self, dados_amenidade):
        nome_amenidade = dados_amenidade['nome'].iloc[0]
        return f'foi da amenidade {nome_amenidade} mais comum'
    
    def titulo_amenidade_menos_comum(self, dados_amenidade):   
        nome_amenidade = dados_amenidade['nome'].iloc[0]
        return f'foi da amenidade {nome_amenidade} menos comum'

    def titulo_amenidade_total(self):
        return f'foi da quantidade total de amenidades'
    
    def formata_quantidade(self, dados_amenidade):
        return format(dados_amenidade['quantidade_amenidade'].iloc[0], ',').replace(',', '.')
