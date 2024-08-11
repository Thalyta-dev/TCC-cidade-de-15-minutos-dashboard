from dados.grafico_queries import *


from pandas import read_sql
from dados.banco_config import BancoDadosUtil

class RepositoryGrafico:
    
    conexao_bd = BancoDadosUtil.estabelecer_conexao_banco()

    def dados_todos_estados(self, modalidade = '1', indice_min=0, indice_max=100, peso_p1=1, peso_p2=1):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_INDICE_BRASIL, con=self.conexao_bd, 
                        params={'modalidade':modalidade, 'indice_min': indice_min, 'indice_max': indice_max, 'peso_p1': peso_p1, 'peso_p2': peso_p2})

    def indice_por_regiao(self, modalidade = '1', peso_p1=1, peso_p2=1):
            return read_sql(sql=GraficoQueriesConstantes.INDICE_POR_REGIAO, con=self.conexao_bd, 
                        params={'modalidade':modalidade, 'peso_p1': peso_p1, 'peso_p2': peso_p2})
        
    def dados_estado(self, modalidade = '1', indice_min=0, indice_max=100, estado=None, peso_p1=1, peso_p2=1):  
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_INDICE_ESTADO, con=self.conexao_bd, 
                        params={ 'estado': estado, 'modalidade':modalidade, 'indice_min': indice_min, 'indice_max': indice_max, 'peso_p1': peso_p1, 'peso_p2': peso_p2})

    def busca_quantidade_total_amenidade(self):
            return read_sql(sql=GraficoQueriesConstantes.QUANTIDADE_TOTAL_AMENIDADE, con=self.conexao_bd)  
      
    def busca_quantidade_total_amenidade_estado(self, estado):
            return read_sql(sql=GraficoQueriesConstantes.QUANTIDADE_TOTAL_AMENIDADE_ESTADO, con=self.conexao_bd, params={ 'estado': estado})    
    
    def busca_quantidade_total_amenidade_municipio(self, municipio):
            return read_sql(sql=GraficoQueriesConstantes.QUANTIDADE_TOTAL_AMENIDADE_MUNICIPIO, con=self.conexao_bd, params={ 'municipio': municipio})
        
    def busca_maior_quantidade_amenidade(self):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_MAIOR_QUANTIDADE_AMENIDADE, con=self.conexao_bd)  
      
    def busca_maior_quantidade_amenidade_estado(self, estado):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_MAIOR_QUANTIDADE_AMENIDADE_ESTADO, con=self.conexao_bd, params={ 'estado': estado})    
    
    def busca_maior_quantidade_amenidade_municipio(self, municipio):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_MAIOR_QUANTIDADE_AMENIDADE_MUNICIPIO, con=self.conexao_bd, params={ 'municipio': municipio})
    
    def busca_menor_quantidade_amenidade(self):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_MENOR_QUANTIDADE_AMENIDADE, con=self.conexao_bd)  
      
    def busca_menor_quantidade_amenidade_estado(self, estado):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_MENOR_QUANTIDADE_AMENIDADE_ESTADO, con=self.conexao_bd, params={ 'estado': estado})    
    
    def busca_menor_quantidade_amenidade_municipio(self, municipio):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_MENOR_QUANTIDADE_AMENIDADE_MUNICIPIO, con=self.conexao_bd, params={ 'municipio': municipio})
    
    def busca_municipios_analisados(self, estado):
        return read_sql(sql=GraficoQueriesConstantes.MUNICIPIOS_ANALISADOS_ESTADO, con=self.conexao_bd, params={ 'estado': estado}) 

    def busca_hexagono_analisados(self, municipio):
        return read_sql(sql=GraficoQueriesConstantes.HEXAGONO_ANALISADOS_MUNICIPIOS, con=self.conexao_bd, params={ 'municipio': municipio}) 

    def busca_status_etapas_municipios(self, estado):
        return read_sql(sql=GraficoQueriesConstantes.STATUS_ETAPA_ESTADO, con=self.conexao_bd, params={ 'estado': estado})  

    def busca_amenidade(self, modalidade):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_AMENIDADE, con=self.conexao_bd,  params={ 'modalidade': modalidade})  
      
    def busca_amenidade_estado(self, estado, modalidade):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_AMENIDADE_ESTADO, con=self.conexao_bd, params={ 'estado': estado, 'modalidade': modalidade})    
    
    def busca_amenidade_municipio(self, municipio, modalidade):
            return read_sql(sql=GraficoQueriesConstantes.BUSCA_AMENIDADE_MUNICIPIO, con=self.conexao_bd, params={ 'municipio': municipio, 'modalidade': modalidade})
    
