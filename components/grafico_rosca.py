import logging
import plotly.graph_objs as go
from dados.grafico_repository import RepositoryGrafico
logger = logging.getLogger('GRAFICO_ROSCA')


class GraficoRosca:
    
    def  __init__(self) -> None:
        self.repository_banco = RepositoryGrafico()

    
    logging.basicConfig(level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    

    def __constroi_grafico_rosca(self, municipio_analisados, legenda):
          
        valores = [municipio_analisados['quantidade_analisadas'].iloc[0], municipio_analisados['quantidade_nao_analisadas'].iloc[0]]

        fig = go.Figure(data=[go.Pie(labels=legenda, values=valores, hole=0.4)]) 
        
        fig.update_layout(
                title_text="Municípios Analisados X Municípios Não Analisados",
                title_x=0.5 
        )
        return fig

    def __constroi_grafico_rosca_hexagonos(self, hexagonos_analisados):
          
        valores = hexagonos_analisados['quantidade'].to_list()
            
        legenda =  hexagonos_analisados['descricao'].to_list()

        fig = go.Figure(data=[go.Pie(labels=legenda, values=valores)]) 
        
        fig.update_layout(
                title_text="Análise Hexágonos",
                title_x=0.5,
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)'           

        )
        
        return fig


        
    def controi_municipio_analisados(self, estado):
        
        logger.info(f'Buscando informações para gerar grafico de rosca de quantidade municípios indice analisados')

        municipio_analisados =self.repository_banco.busca_municipios_analisados(estado=estado)
        legenda = ['Municípios Analisados', 'Múnicipios Não Analisados']
        return self.__constroi_grafico_rosca(municipio_analisados, legenda)
    
    
    def controi_quantidade_hexagono_analisados_brasil(self, modalidade=1):
        
        logger.info(f'Buscando informações para gerar grafico de rosca de quantidade hexagonos analisados')

        hexagonos = self.repository_banco.busca_hexagono_analisados_brasil(modalidade)

        print(hexagonos)
        return self.__constroi_grafico_rosca_hexagonos(hexagonos)
    
    
    def controi_quantidade_hexagono_analisados_estado(self, estado, modalidade=1):
        
        logger.info(f'Buscando informações para gerar grafico de rosca de quantidade hexagonos analisados estado')
        
        hexagonos =self.repository_banco.hexago(estado, modalidade)

        return self.__constroi_grafico_rosca(hexagonos)

    
    def controi_quantidade_hexagono_analisados_municipio(self, municipio, modalidade=1):
        
        logger.info(f'Buscando informações para gerar grafico de rosca de quantidade hexagonos analisados município')

        hexagonos =self.repository_banco.busca_hexagono_analisados_brasil(municipio, modalidade )
        
        return self.__constroi_grafico_rosca(hexagonos)
