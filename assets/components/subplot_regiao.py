import logging
import plotly.express as plot
from pandas import DataFrame
import plotly.graph_objs as go
from utils.mapa_util import MapaUtil
from plotly.subplots import make_subplots
from dados.grafico_repository import RepositoryGrafico
import  pandas as pd
from utils.mapa_util import MapaUtil
import shapely.geometry
import json
logger = logging.getLogger('SUBPLOT')

class SubPlotRegiao:
    
    def __init__(self) -> None:
        self.repository_banco = RepositoryGrafico()
        self.mapaUtil = MapaUtil()

    
    logging.basicConfig(level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
    def __constroi_mapa(self, df_regioes) -> go.Figure:
        
        logger.info(f'Construindo mapa')
        
        df_regioes = self.mapaUtil.convert_gfd(dataframe=df_regioes)
        
        fig = make_subplots(
            rows=1, cols=5,
            subplot_titles=("Norte", "Nordeste", "Sudeste", "Centro-Oeste", "Sul"),
            specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}, {'type': 'choropleth'},{'type': 'choropleth'}, {'type': 'choropleth'}]]
        )

        regions = [
            ('Norte', 1, 1),
            ('Nordeste', 1, 2),
            ('Sudeste', 1, 3),
            ('Centro-oeste', 1, 4),
            ('Sul', 1, 5)
        ]
        
        
        for nome_regiao, row, col in regions:
            geometria_region =  df_regioes.copy()
            geometria_region.loc[df_regioes['regiao'] != nome_regiao, 'indice'] = -1
            fig2 = plot.choropleth(
                geometria_region,
                geojson=geometria_region,
                locations='codigo',
                featureidkey="properties.codigo",
                color='indice',
                hover_data={'regiao'},
                color_continuous_scale=plot.colors.sequential.Plasma,
                range_color=(df_regioes['indice'].min(), df_regioes['indice'].max()), 
                labels={'indice': 'Índice'},
                title=nome_regiao
            )

            fig.update_geos(fitbounds="locations", 
                        visible=False, projection_scale=6, showcountries=True,  
                        countrycolor='black') 
        
            fig.update_layout(
                dragmode=False,  
                hovermode='closest')
            fig.add_trace(
                fig2.data[0],
                row=row, col=col
            )
        
        return fig
    
    def constroi_subplot_brasil(self, modalidade=1, peso_p1=100, peso_p2=100):
        
        logger.info(f'Buscando  informações para gerar subplot das regiões do Brasil')
        
        df_regioes = self.repository_banco.indice_por_regiao(modalidade=modalidade, peso_p1=peso_p1, peso_p2=peso_p2)
        df_regioes['codigo'] = [0,1,2,3,4]
        
        return self.__constroi_mapa(df_regioes)