from utils.exception_util import ExceptionUtil
from utils.yaml_util import YamlUtil

import sqlalchemy

class BancoDadosUtil:

    @staticmethod
    def __recuperar_configuracao_banco() -> dict:
        params_aplicacao = YamlUtil.converter_yaml_para_dict(arquivo_yaml='./resource/application.yml')
        env = params_aplicacao.get("application").get("env")

        return params_aplicacao.get("database").get(env)
    
    @staticmethod
    def estabelecer_conexao_banco() -> sqlalchemy.engine.Connection:
        config = BancoDadosUtil.__recuperar_configuracao_banco()
        url_conexao = f"postgresql+psycopg2://{config.get('username')}:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('name')}"

        try:
            engine = sqlalchemy.create_engine(url=url_conexao)
            conexao_bd = engine.connect()

            return conexao_bd
        except Exception as e:
            raise e
        
    def encerrar_conexao_banco(conexao_bd: sqlalchemy.engine.Connection) -> None:
        try:
            conexao_bd.close()
            conexao_bd.engine.dispose()

        except Exception as e:
            raise e