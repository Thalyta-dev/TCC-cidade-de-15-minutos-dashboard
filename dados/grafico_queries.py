class GraficoQueriesConstantes:
    
    BUSCA_INDICE_BRASIL = '''
        WITH indice_unidade_federativa AS (
            SELECT
                codigo_unidade_federativa,
                codigo_modalidade_transporte,
                nome, 
                sigla, 
                regiao, 
                area_km2, 
                geometria,
                flag_calculo_indice_15min,
                ( %(peso_p1)s * indice_p1 + %(peso_p2)s * indice_p2) / ( %(peso_p1)s + %(peso_p2)s) AS indice
            FROM t_indice_unidade_federativa as i 
            INNER JOIN t_unidade_federativa as m 
            ON i.codigo_unidade_federativa = m.codigo
        )
        SELECT 
            codigo_unidade_federativa,
            codigo_modalidade_transporte,
            nome, 
            sigla, 
            regiao, 
            area_km2, 
            geometria,
            flag_calculo_indice_15min,
            indice
        FROM indice_unidade_federativa
        WHERE codigo_modalidade_transporte = %(modalidade)s
        AND indice > %(indice_min)s AND indice < %(indice_max)s
        '''
        
    BUSCA_INDICE_ESTADO = '''
        WITH indice_unidade_federativa AS (
            SELECT
                codigo, 
                nome, 
                area_km2, 
                geometria,
                codigo_modalidade_transporte, 
                flag_geracao_malha_hexagonal, 
                flag_extracao_amenidades, 
                flag_calculo_matriz_tempo_viagem, 
                flag_calculo_indice_15min, 
                codigo_unidade_federativa,
                ( %(peso_p1)s * indice_p1 + %(peso_p2)s * indice_p2) / ( %(peso_p1)s + %(peso_p2)s) AS indice
            FROM t_indice_municipio as i 
            INNER JOIN t_municipio as m 
            ON i.codigo_municipio = m.codigo
        )
        SELECT 
            codigo, 
            nome, 
            area_km2, 
            geometria, 
            flag_geracao_malha_hexagonal, 
            flag_extracao_amenidades, 
            flag_calculo_matriz_tempo_viagem, 
            flag_calculo_indice_15min, 
            codigo_unidade_federativa,
            indice
        FROM indice_unidade_federativa
        WHERE codigo_modalidade_transporte = %(modalidade)s
        AND indice > %(indice_min)s AND indice < %(indice_max)s
        '''
   
    BUSCA_MENOR_QUANTIDADE_AMENIDADE_ESTADO = '''  
        WITH amenidade_menos_encontrada AS (
            SELECT COUNT(codigo_categoria_pai) AS quantidade_amenidade, codigo_categoria_pai
            FROM t_amenidade_municipio m
            INNER JOIN t_feicao_osm tfo ON m.codigo_feicao_osm = tfo.codigo
            INNER JOIN t_categoria_amenidade tca ON tfo.codigo_categoria_amenidade = tca.codigo
            WHERE codigo_municipio IN (
                SELECT codigo FROM t_municipio WHERE codigo_unidade_federativa = %(estado)s
            )
            GROUP BY codigo_categoria_pai
            ORDER BY quantidade_amenidade ASC
            LIMIT 1
        )

        SELECT
            quantidade_amenidade,
            am.codigo_categoria_pai,
            nome
        FROM amenidade_menos_encontrada AS am
        INNER JOIN t_categoria_amenidade tca ON am.codigo_categoria_pai = tca.codigo;
        '''

    BUSCA_MENOR_QUANTIDADE_AMENIDADE_MUNICIPIO= '''  
        WITH amenidade_menos_encontrada AS (
            SELECT COUNT(codigo_categoria_pai) AS quantidade_amenidade, codigo_categoria_pai
            FROM t_amenidade_municipio m
            INNER JOIN t_feicao_osm tfo ON m.codigo_feicao_osm = tfo.codigo
            INNER JOIN t_categoria_amenidade tca ON tfo.codigo_categoria_amenidade = tca.codigo
            WHERE codigo_municipio =  %(municipio)s
            GROUP BY codigo_categoria_pai
            ORDER BY quantidade_amenidade ASC
            LIMIT 1
        )

        SELECT
            quantidade_amenidade,
            am.codigo_categoria_pai,
            nome
        FROM amenidade_menos_encontrada AS am
        INNER JOIN t_categoria_amenidade tca ON am.codigo_categoria_pai = tca.codigo;
        '''
        
    BUSCA_MAIOR_QUANTIDADE_AMENIDADE_MUNICIPIO= '''  
        WITH amenidade_menos_encontrada AS (
            SELECT COUNT(codigo_categoria_pai) AS quantidade_amenidade, codigo_categoria_pai
            FROM t_amenidade_municipio m
            INNER JOIN t_feicao_osm tfo ON m.codigo_feicao_osm = tfo.codigo
            INNER JOIN t_categoria_amenidade tca ON tfo.codigo_categoria_amenidade = tca.codigo
            WHERE codigo_municipio =  %(municipio)s
            GROUP BY codigo_categoria_pai
            ORDER BY quantidade_amenidade DESC
            LIMIT 1
        )

        SELECT
            quantidade_amenidade,
            am.codigo_categoria_pai,
            nome
        FROM amenidade_menos_encontrada AS am
        INNER JOIN t_categoria_amenidade tca ON am.codigo_categoria_pai = tca.codigo;
        '''

    BUSCA_MAIOR_QUANTIDADE_AMENIDADE_ESTADO = '''  
        WITH amenidade_menos_encontrada AS (
            SELECT COUNT(codigo_categoria_pai) AS quantidade_amenidade, codigo_categoria_pai
            FROM t_amenidade_municipio m
            INNER JOIN t_feicao_osm tfo ON m.codigo_feicao_osm = tfo.codigo
            INNER JOIN t_categoria_amenidade tca ON tfo.codigo_categoria_amenidade = tca.codigo
            WHERE codigo_municipio IN (
                SELECT codigo FROM t_municipio WHERE codigo_unidade_federativa = %(estado)s
            )
            GROUP BY codigo_categoria_pai
            ORDER BY quantidade_amenidade DESC
            LIMIT 1
        )

        SELECT
            quantidade_amenidade,
            am.codigo_categoria_pai,
            nome
        FROM amenidade_menos_encontrada AS am
        INNER JOIN t_categoria_amenidade tca ON am.codigo_categoria_pai = tca.codigo;
'''

    BUSCA_MENOR_QUANTIDADE_AMENIDADE = '''  
        WITH amenidade_menos_encontrada AS (
            SELECT COUNT(codigo_categoria_pai) AS quantidade_amenidade, codigo_categoria_pai
            FROM t_amenidade_municipio m
            INNER JOIN t_feicao_osm tfo ON m.codigo_feicao_osm = tfo.codigo
            INNER JOIN t_categoria_amenidade tca ON tfo.codigo_categoria_amenidade = tca.codigo
            GROUP BY codigo_categoria_pai
            ORDER BY quantidade_amenidade ASC
            LIMIT 1
        )

        SELECT
            quantidade_amenidade,
            am.codigo_categoria_pai,
            nome
        FROM amenidade_menos_encontrada AS am
        INNER JOIN t_categoria_amenidade tca ON am.codigo_categoria_pai = tca.codigo;
'''

    BUSCA_MAIOR_QUANTIDADE_AMENIDADE = '''  
        WITH amenidade_menos_encontrada AS (
            SELECT  COUNT(codigo_categoria_pai) AS quantidade_amenidade, codigo_categoria_pai
            FROM t_amenidade_municipio m
            INNER JOIN t_feicao_osm tfo ON m.codigo_feicao_osm = tfo.codigo
            INNER JOIN t_categoria_amenidade tca ON tfo.codigo_categoria_amenidade = tca.codigo
            GROUP BY codigo_categoria_pai
            ORDER BY quantidade_amenidade DESC
            LIMIT 1
        )

        SELECT
            quantidade_amenidade,
            am.codigo_categoria_pai,
            nome
        FROM amenidade_menos_encontrada AS am
        INNER JOIN t_categoria_amenidade tca ON am.codigo_categoria_pai = tca.codigo;
    '''

    QUANTIDADE_TOTAL_AMENIDADE_ESTADO = '''
    
        SELECT COUNT(*) as quantidade_amenidade
        FROM t_amenidade_municipio where codigo_municipio IN (
            SELECT codigo FROM t_municipio where codigo_unidade_federativa =  %(estado)s)
    '''
    QUANTIDADE_TOTAL_AMENIDADE_MUNICIPIO = '''
        SELECT COUNT(*) as quantidade_amenidade
        FROM t_amenidade_municipio where codigo_municipio =  %(municipio)s
    '''
    
    QUANTIDADE_TOTAL_AMENIDADE = '''
        SELECT COUNT(*) as quantidade_amenidade
        FROM t_amenidade_municipio
    '''
    
    MUNICIPIOS_ANALISADOS_ESTADO = '''SELECT 
        SUM(CASE 
            WHEN flag_geracao_malha_hexagonal = 'C' AND
                flag_extracao_amenidades = 'C' AND
                flag_calculo_matriz_tempo_viagem = 'C' AND
                flag_calculo_indice_15min = 'C' 
            THEN 1
            ELSE 0
        END) AS quantidade_analisadas,

        SUM(CASE 
            WHEN flag_geracao_malha_hexagonal != 'C' OR
                flag_extracao_amenidades != 'C' OR
                flag_calculo_matriz_tempo_viagem != 'C' OR
                flag_calculo_indice_15min != 'C'
            THEN 1
            ELSE 0
        END) AS quantidade_nao_analisadas
    FROM t_municipio
    where codigo_unidade_federativa = %(estado)s'''
    
    HEXAGONO_ANALISADOS_MUNICIPIOS = '''SELECT 
        COUNT(*) quantidade_analisadas,
        SUM(CASE 
            WHEN indice_p1 is not null
            THEN 1
            ELSE 0
        end) AS quantidade_analisadas
        FROM
        t_indice_hexagono i  
        RIGHT  join t_malha_hexagonal_municipio m 
        ON i.codigo_hexagono =m.codigo 
        WHERE m.codigo_municipio  = %(MUNICIPIO)s'''
    
    STATUS_ETAPA_ESTADO= '''SELECT 
        nome,
        CASE 
            WHEN flag_geracao_malha_hexagonal = 'C' THEN 'CONCLUÍDO'
            ELSE 'FALHA'
        END AS geracao_malha_hexagonal_status,

        CASE 
            WHEN flag_extracao_amenidades = 'C' THEN 'CONCLUÍDO'
            ELSE 'FALHA'
        END AS extracao_amenidades_status,

        CASE 
            WHEN flag_calculo_matriz_tempo_viagem = 'C' THEN 'CONCLUÍDO'
            ELSE 'FALHA'
        END AS calculo_matriz_tempo_viagem_status,

        CASE 
            WHEN flag_calculo_indice_15min = 'C' THEN 'CONCLUÍDO'
            ELSE 'FALHA'
        END AS calculo_indice_15min_status

    FROM t_municipio where codigo_unidade_federativa = %(estado)s'''
    
    
    INDICE_POR_REGIAO = '''WITH indice_unidade_federativa AS (
            SELECT
                codigo_unidade_federativa,
                codigo_modalidade_transporte,
                nome, 
                sigla, 
                regiao, 
                area_km2, 
                geometria,
                flag_calculo_indice_15min,
                ( %(peso_p1)s * indice_p1 + 1 *  %(peso_p2)s) / (  %(peso_p1)s +  %(peso_p2)s) AS indice
            FROM t_indice_unidade_federativa as i 
            INNER JOIN t_unidade_federativa as m 
            ON i.codigo_unidade_federativa = m.codigo
        )
        SELECT 
            regiao, 
             ST_Union(geometria) as geometria, 
            avg(indice) as indice
        FROM indice_unidade_federativa
        WHERE codigo_modalidade_transporte =  %(modalidade)s
        group by regiao'''
        
    BUSCA_AMENIDADE_ESTADO= '''  
        SELECT 
            COUNT(DISTINCT matriz.codigo_amenidade) AS contagem,
            uf.codigo,
            categoria.nome AS categoria
        FROM t_matriz_tempo_viagem AS matriz
        INNER JOIN t_amenidade_municipio AS amenidade
            ON matriz.codigo_amenidade = amenidade.codigo
        INNER JOIN t_feicao_osm AS feicao
            ON amenidade.codigo_feicao_osm = feicao.codigo
        INNER JOIN t_categoria_amenidade AS categoria
            ON feicao.codigo_categoria_amenidade = categoria.codigo
        INNER JOIN t_municipio AS municipio
            ON municipio.codigo = amenidade.codigo_municipio
        INNER JOIN t_unidade_federativa AS uf
            ON municipio.codigo_unidade_federativa = uf.codigo
        WHERE matriz.tempo_viagem_seg <= 900
            AND uf.codigo = %(estado)s
            AND matriz.codigo_modalidade_transporte = %(modalidade)s
        GROUP BY categoria.nome, uf.codigo;
    '''

    BUSCA_AMENIDADE_MUNICIPIO = '''  
        SELECT 
            COUNT(DISTINCT matriz.codigo_amenidade) AS contagem,
            municipio.codigo_municipio,
            nome AS categoria
        FROM t_matriz_tempo_viagem matriz
        INNER JOIN t_amenidade_municipio amenidade
            ON matriz.codigo_amenidade = amenidade.codigo
        INNER JOIN t_feicao_osm feicao
            ON amenidade.codigo_feicao_osm = feicao.codigo
        INNER JOIN t_categoria_amenidade categoria
            ON feicao.codigo_categoria_amenidade = categoria.codigo
        INNER JOIN t_amenidade_municipio municipio
            ON feicao.codigo = municipio.codigo_feicao_osm 
        WHERE matriz.tempo_viagem_seg <= 900 AND municipio.codigo_municipio = %(municipio)s
        AND matriz.codigo_modalidade_transporte = %(modalidade)s
        GROUP BY nome, municipio.codigo_municipio
    '''

    BUSCA_AMENIDADE = '''  
        SELECT 
	        COUNT(DISTINCT matriz.codigo_amenidade) AS contagem,
	        nome AS categoria
        FROM t_matriz_tempo_viagem matriz
        INNER JOIN t_amenidade_municipio amenidade
	    ON matriz.codigo_amenidade = amenidade.codigo
        INNER JOIN t_feicao_osm feicao
	    ON amenidade.codigo_feicao_osm = feicao.codigo
        INNER JOIN t_categoria_amenidade categoria
	    ON feicao.codigo_categoria_amenidade = categoria.codigo
        WHERE matriz.tempo_viagem_seg <= 900
            AND matriz.codigo_modalidade_transporte = %(modalidade)s
        GROUP BY  nome
    '''
