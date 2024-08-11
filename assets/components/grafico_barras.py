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
    
    def __constroi_grafico_barra(self, dados_grafico: DataFrame, titulo: str) -> go.Figure:
        
        logger.info(f'Construindo grafico de barras')

        fig = plot.bar(
            dados_grafico,
            text_auto='.2f',
            x='nome', 
            y='indice',
            labels={'nome': 'Estados', 'indice': 'Índice de cidade de 15 minutos'},
            title=titulo
        )
        
        fig.update_yaxes(range=[0, dados_grafico['indice'].max()])
    
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        '''fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='white'), 
        title_font=dict(color='white'), 
        xaxis=dict(title_font=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(
            title_font=dict(color='white'),
            tickfont=dict(color='white'),
            nticks=10,
            range=[0, 100],
        ), 
        coloraxis_colorbar=dict(tickfont=dict(color='white'), titlefont=dict(color='white'))  
        )'''
        
        logger.info(f'Grafico construido')
        return fig 
        
    def controi_grafico_brasil_maior_indice(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=100, peso_p2=100):
        
        logger.info(f'Buscando informações para gerar grafico maior indice do Brasil')

        indice_brasil = self.repository_banco.dados_todos_estados(modalidade=modalidade,
                                                        indice_min=indice_min, 
                                                        indice_max=indice_max,
                                                        peso_p1=peso_p1, peso_p2=peso_p2
                                                        )
        indice_brasil = pd.DataFrame(indice_brasil)
        indice_brasil = indice_brasil.sort_values(by='indice', ascending=False)
        indice_brasil = indice_brasil.head(5)
        
        return self.__constroi_grafico_barra(indice_brasil, 'Estados com maior Índice de Cidade de 15 minutos')

    def controi_grafico_brasil_menor_indice(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=100, peso_p2=100):
        
        logger.info(f'Buscando informações para gerar grafico menor indice do Brasil')

        indice_brasil = self.repository_banco.dados_todos_estados(modalidade=modalidade,
                                                        indice_min=indice_min, 
                                                        indice_max=indice_max, 
                                                        peso_p1=peso_p1, 
                                                        peso_p2=peso_p2)
        indice_brasil = pd.DataFrame(indice_brasil)
        indice_brasil = indice_brasil.sort_values(by='indice', ascending=True)
        indice_brasil = indice_brasil.head(5)
        
        return self.__constroi_grafico_barra(indice_brasil, 'Estados com menor Índice de Cidade de 15 minutos')

    def controi_grafico_estado_maior_indice(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=100, peso_p2=100, estado= None):
        
        logger.info(f'Buscando informações para gerar grafico maior indice do estado')

        indice_brasil = self.repository_banco.dados_estado(modalidade=modalidade,
                                                        indice_min=indice_min, 
                                                        indice_max=indice_max,
                                                        peso_p1=peso_p1,
                                                        peso_p2=peso_p2,
                                                        estado=estado
                                                        )
        indice_brasil = pd.DataFrame(indice_brasil)
        indice_brasil = indice_brasil.sort_values(by='indice', ascending=False)
        indice_brasil = indice_brasil.head(10)
        
        return self.__constroi_grafico_barra(indice_brasil, 'Municípios com maior Índice de Cidade de 15 minutos')

    def controi_grafico_estado_menor_indice(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=100, peso_p2=100, estado=None):
        
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
    
        return self.__constroi_grafico_barra(indice_brasil, 'Municípios com menor Índice de Cidade de 15 minutos')