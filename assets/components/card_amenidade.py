import logging
from dados.grafico_repository import RepositoryGrafico
logger = logging.getLogger('AMENIDADES')
from utils.amenidades_util import AmenidadeUtil

class CardAmenidades:
    
    def  __init__(self) -> None:
        self.repository_banco = RepositoryGrafico()
        self.amenidades_util = AmenidadeUtil()


    logging.basicConfig(level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    def constroi_amenidades_brasil(self):
        
        logger.info(f'Constroi amenidades brasil')

        quantidade_total_amenidade = self.repository_banco.busca_quantidade_total_amenidade()
        amenidade_mais_comum = self.repository_banco.busca_maior_quantidade_amenidade()
        amenidade_menos_comum = self.repository_banco.busca_menor_quantidade_amenidade()
        
        return self.__constroi_titulo_amenidades(quantidade_total_amenidade, amenidade_mais_comum, amenidade_menos_comum)

    def constroi_amenidades_estado(self, estado:str):
        
        logger.info(f'Constroi amenidades estado')

        quantidade_total_amenidade = self.repository_banco.busca_quantidade_total_amenidade_estado(estado=estado)
        amenidade_mais_comum = self.repository_banco.busca_maior_quantidade_amenidade_estado(estado=estado)
        amenidade_menos_comum = self.repository_banco.busca_menor_quantidade_amenidade_estado(estado=estado)
        
        return self.__constroi_titulo_amenidades(quantidade_total_amenidade, amenidade_mais_comum, amenidade_menos_comum)

    def amenidades_municipio(self, municipio:str):
        
        logger.info(f'Constroi amenidades municipio')

        quantidade_total_amenidade = self.repository_banco.busca_quantidade_total_amenidade_municipio(municipio=municipio)
        amenidade_mais_comum = self.repository_banco.busca_maior_quantidade_amenidade_municipio(municipio=municipio)
        amenidade_menos_comum = self.repository_banco.busca_menor_quantidade_amenidade_municipio(municipio=municipio)
    
        return self.__constroi_titulo_amenidades(quantidade_total_amenidade, amenidade_mais_comum, amenidade_menos_comum)


    def __constroi_titulo_amenidades(self, quantidade_total_amenidade, amenidade_mais_comum, amenidade_menos_comum):
        quantidade_total_amenidade['titulo'] = self.amenidades_util.titulo_amenidade_total()
        quantidade_total_amenidade['quantidade_amenidade'] = self.amenidades_util.formata_quantidade(quantidade_total_amenidade)
        amenidade_mais_comum['titulo'] = self.amenidades_util.titulo_amenidade_mais_comum(amenidade_mais_comum)
        amenidade_mais_comum['quantidade_amenidade'] = self.amenidades_util.formata_quantidade(amenidade_mais_comum)
        amenidade_menos_comum['titulo'] = self.amenidades_util.titulo_amenidade_menos_comum(amenidade_menos_comum)
        amenidade_menos_comum['quantidade_amenidade'] = self.amenidades_util.formata_quantidade(amenidade_menos_comum)
        return quantidade_total_amenidade, amenidade_mais_comum, amenidade_menos_comum