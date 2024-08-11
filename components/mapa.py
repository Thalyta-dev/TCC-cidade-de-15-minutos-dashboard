import logging
import plotly.express as plot
from pandas import DataFrame
import plotly.graph_objs as go
from utils.mapa_util import MapaUtil
from dados.mapa_repository import RepositoryMapa
logger = logging.getLogger('MAPA')

class Mapa:
    
    def __init__(self) -> None:
        self.repository_banco = RepositoryMapa()
        self.mapaUtil = MapaUtil()

    
    logging.basicConfig(level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
    def __constroi_mapa(self, geometria_indice: DataFrame) -> go.Figure:
        
        logger.info(f'Construindo mapa')

        geometria_indice = self.mapaUtil.convert_gfd(dataframe=geometria_indice)

        geometria_indice.fillna(-1, inplace=True)
        logger.info(f'Plotando mapa')

        fig = plot.choropleth(geometria_indice, geojson=geometria_indice[['geometry', 'indice', 'nome', 'codigo']],
                    color="indice",
                    locations="codigo", featureidkey="properties.codigo",
                    projection="mercator",
                    hover_data={'nome'},
                    scope="south america",
                    range_color=(0, geometria_indice['indice'].max()), 
                    labels={'Indice':'Indice'}
                )
        
        fig.update_geos(fitbounds="locations", 
                        visible=False,)
        
        fig.update_layout(
            dragmode=False,  
            hovermode='closest',
            coloraxis_colorbar={'len': 0.5,'yanchor': 'middle','y': 0.5},
            width=1200,
            height=900,
        )
        
        logger.info(f'Mapa construido')
        return  fig
    
    def constroi_mapa_brasil(self, modalidade=1, indice_min=0, indice_max=100, peso_p1=100, peso_p2=100):
        
        logger.info(f'Buscando  informações para gerar mapa do Brasil')
        
        indice_dos_estados = self.repository_banco.buscar_indice_estados(modalidade=modalidade, 
                                                     indice_min=indice_min, 
                                                     indice_max=indice_max,
                                                     peso_p1=peso_p1,
                                                     peso_p2=peso_p2)   
        
        geometria_estados = self.repository_banco.buscar_geometria_estado()
        geometria_indice = geometria_estados.merge(indice_dos_estados, how='left', left_on='codigo', right_on='codigo_unidade_federativa')
        return self.__constroi_mapa(geometria_indice)
    
    def constroi_mapa_estado(self, estado = None, modalidade=1, indice_min=0, indice_max=100, peso_p1=100, peso_p2=100):
        
        logger.info(f'Buscando  informações para gerar mapa do estado de codigo: {estado}')
        
        indice_municipios = self.repository_banco.buscar_indice_municipios(
            estado=estado,
            peso_p1=peso_p1,
            peso_p2=peso_p2,
            modalidade=modalidade,
            indice_min=indice_min,
            indice_max=indice_max)
                
        geometria_municipios = self.repository_banco.buscar_geometria_municipios(estado=estado)
        geometria_indice = geometria_municipios.merge(indice_municipios, how='left', left_on='codigo', right_on='codigo_municipio')
        return self.__constroi_mapa(geometria_indice)
        
    def constroi_mapa_municipio(self, municipio = None, modalidade=1, indice_min=0, indice_max=100, peso_p1=100, peso_p2=100):
        
        logger.info(f'Buscando  informações para gerar mapa do município de codigo: {municipio}')

        indice_hexagono = self.repository_banco.buscar_indice_hexagono(municipio=municipio, 
                                                            modalidade=modalidade, 
                                                            indice_min=indice_min, 
                                                            indice_max=indice_max,
                                                            peso_p1=peso_p1,
                                                            peso_p2=peso_p2)
        hexagono_em_municipios = self.repository_banco.buscar_geometria_hexagonos(municipio=municipio)        

        geometria_indice = hexagono_em_municipios.merge(indice_hexagono, how='left', left_on='codigo', right_on='codigo')
        return self.__constroi_mapa(geometria_indice)