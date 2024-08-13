import logging
import plotly.express as plot
from pandas import DataFrame
import plotly.graph_objs as go
from dados.grafico_repository import RepositoryGrafico
logger = logging.getLogger('TABELA')

class TabelaEtapas:
    
      def __init__(self) -> None:
        self.repository_banco = RepositoryGrafico()

      logging.basicConfig(level=logging.DEBUG,  
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
  
      def __constroi_tabelas_erros_municipios(self, tabela: DataFrame) -> go.Figure:

            fig = go.Figure(data=[go.Table(
                  header=dict(values=list(tabela.columns),
                              #fill_color='#636EFA',  
                              #line_color='white',
                              #font_color='white',
                              font_size = 15,
                              height=40,
                              align='center'),
                  cells=dict(values=[tabela[col] for col in tabela.columns],
                              #fill_color='#636EFA',  
                              #line_color='white',
                              #font_color='white',
                              height=30,
                              align='left'))
            ])
            
            fig.update_layout(
                  title_text="Status de cada etapa de processamento dos municípios", paper_bgcolor='rgba(0,0,0,0)')

            logger.info(f' Tabela de etapa de processamento concluida')

            return fig

      def constroi_tabela_municipio(self, estado: str):
            logger.info(f'Construindo tabela de etapa de processamento')
            tabela = self.repository_banco.busca_status_etapas_municipios(estado=estado)
            return self.__constroi_tabelas_erros_municipios(tabela=tabela)