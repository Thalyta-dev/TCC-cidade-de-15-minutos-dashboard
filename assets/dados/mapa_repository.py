from dados.mapa_queries import MapaQueriesConstantes
from geoalchemy2 import Geometry
from sqlalchemy import func

from pandas import read_sql
from sqlalchemy.engine import Connection
from dados.banco_config import BancoDadosUtil

class RepositoryMapa:
    
    conexao_bd = BancoDadosUtil.estabelecer_conexao_banco()

    def buscar_indice_estados(self, modalidade, indice_min, indice_max, peso_p1, peso_p2):
        return read_sql(sql=MapaQueriesConstantes.CALCULAR_ESTADOS, con=self.conexao_bd, 
                        params={'modalidade':modalidade, 'indice_min': indice_min, 'indice_max': indice_max, 'peso_p1': peso_p1, 'peso_p2': peso_p2})
        
    def buscar_indice_municipios(self, estado, modalidade, indice_min, indice_max, peso_p1, peso_p2):
        return read_sql(sql=MapaQueriesConstantes.CALCULAR_MUNICIPIOS, con=self.conexao_bd, 
                        params={ 'estado': estado, 'modalidade':modalidade, 'indice_min': indice_min, 'indice_max': indice_max, 'peso_p1': peso_p1, 'peso_p2': peso_p2})
        
    def buscar_indice_hexagono(self, municipio, modalidade, indice_min, indice_max, peso_p1, peso_p2):
        return read_sql(sql=MapaQueriesConstantes.CALCULAR_HEXAGONO, con=self.conexao_bd,
                        params={ 'municipio': municipio,'modalidade':modalidade, 'indice_min': indice_min, 'indice_max': indice_max, 'peso_p1': peso_p1, 'peso_p2': peso_p2})
        
    def buscar_geometria_municipios(self, estado): 
        return read_sql(sql=MapaQueriesConstantes.GEOMETRIA_MUNICIPIO, con=self.conexao_bd, params={'estado': estado}) 
    
    def buscar_geometria_estado(self): 
        return read_sql(sql=MapaQueriesConstantes.GEOMETRIA_ESTADOS, con=self.conexao_bd) 
    
    def buscar_geometria_hexagonos(self, municipio): 
        return read_sql(sql=MapaQueriesConstantes.GEOMETRIA_HEXAGONO,  params={'municipio': municipio}, con=self.conexao_bd)