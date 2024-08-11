import logging
import plotly.graph_objs as go
from dados.grafico_repository import RepositoryGrafico
logger = logging.getLogger('GRAFICO_ROSCA')


class GraficoRosca:
    
    def  __init__(self) -> None:
        self.repository_banco = RepositoryGrafico()

    
    logging.basicConfig(level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    

    def constroi_grafico_rosca_estado(self,estado:str):
  
        municipio_analisados =self.repository_banco.busca_municipios_analisados(estado=estado)
        
        valores = [municipio_analisados['quantidade_analisadas'].iloc[0], municipio_analisados['quantidade_nao_analisadas'].iloc[0]]
        nomes = ['Municípios Analisados', 'Múnicipios Não Analisados']

        fig = go.Figure(data=[go.Pie(labels=nomes, values=valores, hole=0.4)]) 
        
        '''fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(color='white'), 
                legend_font=dict(color='white'), 
                title_text="Municípios Analizados X Municípios Não Analizados",
                title_x=0.5 
        )'''
        return fig

