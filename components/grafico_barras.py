import logging
import pandas as pd
import plotly.express as plot
from pandas import DataFrame
import plotly.graph_objs as go
from dados.grafico_repository import RepositoryGrafico
logger = logging.getLogger('GRAFICO_BARRAS')


class GraficoBarra:
    
    def  __init__(self) -> None:
        self.repository_banco = RepositoryGrafico()

    logging.basicConfig(level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    def __constroi_grafico_barra(self, dados_grafico: DataFrame, titulo: str, label: str) -> go.Figure:
        
        logger.info(f'Construindo grafico de barras')

        fig = plot.bar(
            dados_grafico,
            text_auto='.2f',
            x='nome', 
            y='indice',
            labels={'nome': label, 'indice': 'Índice de Conformidade'},
            title=titulo
        )
        
        fig.update_yaxes(range=[0, dados_grafico['indice'].max()])
    
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        logger.info(f'Grafico construido')
        return fig 
        
    def controi_grafico_brasil_maior_indice(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=1, peso_p2=1):
        
        logger.info(f'Buscando informações para gerar grafico maior indice do Brasil')

        indice_brasil = self.repository_banco.dados_todos_estados(modalidade=modalidade,
                                                        indice_min=indice_min, 
                                                        indice_max=indice_max,
                                                        peso_p1=peso_p1, peso_p2=peso_p2
                                                        )
        indice_brasil = pd.DataFrame(indice_brasil)
        indice_brasil = indice_brasil.sort_values(by='indice', ascending=False)
        indice_brasil = indice_brasil.head(5)
        
        return self.__constroi_grafico_barra(indice_brasil, 'Estados Com Maiores Índice de Conformidade', 'Estados')

    def controi_grafico_brasil_menor_indice(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=1, peso_p2=1):
        
        logger.info(f'Buscando informações para gerar grafico menor indice do Brasil')

        indice_brasil = self.repository_banco.dados_todos_estados(modalidade=modalidade,
                                                        indice_min=indice_min, 
                                                        indice_max=indice_max, 
                                                        peso_p1=peso_p1, 
                                                        peso_p2=peso_p2)
        indice_brasil = pd.DataFrame(indice_brasil)
        indice_brasil = indice_brasil.sort_values(by='indice', ascending=True)
        indice_brasil = indice_brasil.head(5)
        
        return self.__constroi_grafico_barra(indice_brasil, 'Estados Com Menores Índice de Conformidade', 'Estados')

    def controi_grafico_estado_maior_indice(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=1, peso_p2=1, estado= None):
        
        logger.info(f'Buscando informações para gerar grafico maior indice do estado')

        indice_brasil = self.repository_banco.dados_estado(modalidade=modalidade,
                                                        indice_min=indice_min, 
                                                        indice_max=indice_max,
                                                        peso_p1=peso_p1,
                                                        peso_p2=peso_p2,
                                                        estado=estado
                                                        )
        indice_brasil = pd.DataFrame(indice_brasil)
        print(indice_brasil)
        indice_brasil = indice_brasil.sort_values(by='indice', ascending=False)
        indice_brasil = indice_brasil.head(10)
        
        return self.__constroi_grafico_barra(indice_brasil, 'Municípios Com Maiores Índice de Conformidade', 'Municípios')

    def controi_grafico_estado_menor_indice(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=1, peso_p2=1, estado=None):
        
        logger.info(f'Buscando informações para gerar grafico menor indice do estado')

        indice_brasil = self.repository_banco.dados_estado(modalidade=modalidade,
                                                        indice_min=indice_min, 
                                                        indice_max=indice_max, 
                                                        estado=estado,
                                                        peso_p1=peso_p1, 
                                                        peso_p2=peso_p2)
        indice_brasil = pd.DataFrame(indice_brasil)
        indice_brasil = indice_brasil.sort_values(by='indice', ascending=True)
        indice_brasil = indice_brasil.head(10)
    
        return self.__constroi_grafico_barra(indice_brasil, 'Municípios Com Menores Índice de Conformidade', label = 'Municípios')
    
    def controi_grafico_amenidade_por_regiao(self):
        
        logger.info(f'Buscando informações para gerar grafico amenidade por região ')

        amenidade_por_regiao = self.repository_banco.busca_amenidade_por_regiao()
        
        lista_dict_regiao = ({
            'Centro-oeste': [],
            'Nordeste': [],
            'Norte': [],
            'Sudeste': [],
            'Sul': []
        })

        for registro in amenidade_por_regiao.to_numpy():
            lista_dict_regiao.get(registro[0]).append(registro[2])

        df_amenidade_regiao = DataFrame(lista_dict_regiao, index=['Alimentação', 'Compras e Serviços', 'Cultura, Esportes e Lazer', 'Educação', 'Saúde', 'Trabalho', 'Transporte'])
    
        df_amenidade_regiao = df_amenidade_regiao.reset_index().melt(id_vars='index', var_name='Região', value_name='Quantidade')
        df_amenidade_regiao.rename(columns={'index': 'Categoria'}, inplace=True)
                
        fig = plot.bar(
            df_amenidade_regiao,
            x='Categoria', 
            y='Quantidade',
            text_auto=True,
            color='Região', 
            barmode='group',
            labels={'nome': 'Categoria Amenidades', 'quantidade': 'Quantidade Amenidade'},
            title="Amenidade por região"
        )
        
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            height=700

        )
        return fig