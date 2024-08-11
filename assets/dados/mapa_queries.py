class MapaQueriesConstantes:

    CALCULAR_ESTADOS = '''
        WITH indice_unidade_federativa AS (
            SELECT
                codigo_unidade_federativa,
                codigo_modalidade_transporte,
                ( %(peso_p1)s * indice_p1 + %(peso_p2)s * indice_p2) / ( %(peso_p1)s + %(peso_p2)s) AS indice
            FROM t_indice_unidade_federativa
        )
        SELECT 
            codigo_unidade_federativa,
            codigo_modalidade_transporte,
            indice
        FROM indice_unidade_federativa
        WHERE codigo_modalidade_transporte = %(modalidade)s
        AND indice > %(indice_min)s AND indice < %(indice_max)s
        
    '''
    CALCULAR_MUNICIPIOS = '''
        WITH indice_municipio AS (
            SELECT
                i.codigo_municipio, 
                i.codigo_modalidade_transporte, 
                m.nome,
                m.codigo_unidade_federativa,
                (%(peso_p1)s * indice_p1 + %(peso_p2)s * indice_p2) / ( %(peso_p1)s + %(peso_p2)s) AS indice
            FROM public.t_municipio AS m
            INNER JOIN public.t_indice_municipio AS i 
            ON i.codigo_municipio = m.codigo
        )
        SELECT 
            codigo_municipio,
            codigo_modalidade_transporte,
            indice
        FROM indice_municipio
        WHERE codigo_modalidade_transporte = %(modalidade)s
        AND  codigo_unidade_federativa = %(estado)s
        AND indice > %(indice_min)s AND indice < %(indice_max)s
    '''
    CALCULAR_HEXAGONO = '''
    
        WITH indice_hexagono AS (
            SELECT
                m.codigo_municipio, 
                i.codigo_modalidade_transporte,
                m.codigo,
                m.hexagono_h3 as nome,
                (%(peso_p1)s * indice_p1 + %(peso_p2)s * indice_p2) / ( %(peso_p1)s + %(peso_p2)s) AS indice
            FROM public.t_malha_hexagonal_municipio AS m
            INNER JOIN public.t_indice_hexagono AS i 
            ON i.codigo_hexagono = m.codigo
        )
        SELECT 
        
            codigo_municipio,
            codigo_modalidade_transporte,
            indice,
            codigo,
            nome
        FROM indice_hexagono
        WHERE codigo_modalidade_transporte = %(modalidade)s
        AND  codigo_municipio = %(municipio)s
        AND indice > %(indice_min)s AND indice < %(indice_max)s
    '''
    GEOMETRIA_HEXAGONO = '''
        SELECT codigo, ST_AsText(geometria) as geometry, codigo_municipio
        FROM public.t_malha_hexagonal_municipio where codigo_municipio =  %(municipio)s  
    '''
    GEOMETRIA_MUNICIPIO = '''
    SELECT codigo,nome,area_km2, ST_AsText(ST_Simplify(geometria, 0.001)) as geometry, flag_geracao_malha_hexagonal, codigo_unidade_federativa
	FROM public.t_municipio where codigo_unidade_federativa =  %(estado)s  
    '''
    GEOMETRIA_ESTADOS = '''
    SELECT codigo, nome, sigla, ST_AsText(ST_Simplify(geometria, 0.001)) as geometry
	FROM public.t_unidade_federativa  
    '''