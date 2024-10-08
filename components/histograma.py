import logging
import plotly.express as plot
from pandas import DataFrame
import plotly.graph_objs as go
from dados.grafico_repository import RepositoryGrafico
logger = logging.getLogger('HISTOGRAMA')

class Histrograma:
    
    def __init__(self) -> None:
        self.repository_banco = RepositoryGrafico()

    logging.basicConfig(level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
    def __constroi_histograma(self, dados_amenidade: DataFrame, titulo: str) -> go.Figure:
        
        logger.info(f'Construindo histograma')

        max_contagem = dados_amenidade['contagem'].max()
        min_contagem = dados_amenidade['contagem'].min()
        
        dados_amenidade['Categorias'] = dados_amenidade['contagem'].apply(lambda x: 'maior' if x == max_contagem 
                                                                             else ('menor' if x == min_contagem else 'outras'))
        fig = plot.histogram(
                dados_amenidade, 
                x="categoria", 
                y='contagem', 
                text_auto=True,
                log_y=True,
                color='Categorias',
                title=titulo,
                color_discrete_map={
                    "Mais comum": "green",
                    "Mais comum": "red",  
                    "Outras": "blue" 
            }
        )
        
        fig.update_layout(bargap=0.1,
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_title="Categoria de Amenidades",
                            yaxis_title="Quantidade",)
        
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

        fig.update_layout(
        yaxis=dict(
            nticks=10
        ), 
        )
        return fig
    
    def constroi_histograma_brasil(self, modalidade=1):
        
        logger.info(f'Buscando informações para gerar histograma do Brasil')
        
        amenidades_brasil = self.repository_banco.busca_amenidade(modalidade=modalidade)

        titulo = 'Contagem por subcategoria de amenidade'
        
        fig = self.__constroi_histograma(amenidades_brasil, titulo)
        fig.update_layout(bargap=0.1,
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_title="Subcategoria de Amenidades",
                            yaxis_title="Quantidade",
                            height=900)
        return fig
    
    def constroi_histograma_estado(self, estado=None, modalidade=1):
        
        logger.info(f'Buscando informações para gerar histograma do estado ')
        
        amenidade_estado = self.repository_banco.busca_amenidade_estado(modalidade=modalidade, estado=estado)

        titulo = 'Contagem por subcategoria de amenidade do estado '
        
        fig = self.__constroi_histograma(amenidade_estado, titulo)
        fig.update_layout(bargap=0.1,
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Subcategoria de Amenidades",
                    yaxis_title="Quantidade",
                    height=900)
        return fig
    
    def constroi_histograma_municipio(self, municipio=None, modalidade=1):
        
        logger.info(f'Buscando informações para gerar histograma do município {municipio}')
        
        amenidade_municipio = self.repository_banco.busca_amenidade_municipio(modalidade=modalidade, municipio=municipio)

        logger.info(f'{amenidade_municipio}')

        titulo = 'Contagem por subcategoria de amenidade do municipio'

        fig = self.__constroi_histograma(amenidade_municipio, titulo)
        
        fig.update_layout(bargap=0.1,
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Subcategoria de Amenidades",
                    yaxis_title="Quantidade",
                    height=900)
        return fig

    def constroi_histograma_quantidade_amenidades_brasil(self):
        
        logger.info(f'Buscando informações para gerar histograma do Brasil')
        
        amenidades_brasil = self.repository_banco.busca_quantidade_amedidade_por_categoria()

        titulo = 'Contagem por categoria de amenidade'
        return self.__constroi_histograma(amenidades_brasil, titulo)
    
    def constroi_histograma_quantidade_amenidades_estado(self, estado=None, modalidade=1):
        
        logger.info(f'Buscando informações para gerar histograma do estado ')
        
        amenidade_estado = self.repository_banco.busca_quantidade_amedidade_por_categoria_estado(estado)

        titulo = 'Contagem por categoria de amenidade do estado '
        
        return self.__constroi_histograma(amenidade_estado, titulo)
    
    def constroi_histograma_quantidade_amenidades_municipio(self, municipio=None, modalidade=1):
        
        logger.info(f'Buscando informações para gerar histograma do município {municipio}')
        
        amenidade_municipio = self.repository_banco.busca_quantidade_amedidade_por_categoria_municipio(municipio)

        titulo = 'Contagem por categoria de amenidade do municipio'

        return self.__constroi_histograma(amenidade_municipio, titulo)