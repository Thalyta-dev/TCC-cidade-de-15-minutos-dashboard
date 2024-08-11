
import pandas as pd

class FormUtil:
       
    df_estados = pd.read_csv('dataset/estados.csv')
    df_municipios = pd.read_csv('dataset/municipios.csv', encoding='utf-8')
    indices = [0, 20, 40, 60, 80, 100]
    

    @staticmethod
    def dic_estados():
        return dict(zip(FormUtil.df_estados['NOME'], FormUtil.df_estados['COD'])) 
       
    @staticmethod
    def dic_municipios():
        return dict(zip(FormUtil.df_municipios['NOME'], FormUtil.df_municipios['COD']))
       
    @staticmethod
    def array_indice():
        return FormUtil.indices
