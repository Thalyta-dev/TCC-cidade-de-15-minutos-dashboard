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
            regiao as região, 
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
    
    STATUS_ETAPA_ESTADO= '''
        SELECT 
            nome as Município,
        CASE 
            WHEN flag_geracao_malha_hexagonal = 'C' THEN 'CONCLUÍDO'
            ELSE 'FALHA'
        END AS "Geração malha hexagonal" ,
        CASE 
            WHEN flag_extracao_amenidades = 'C' THEN 'CONCLUÍDO'
            ELSE 'FALHA'
        END AS "Extração das amenidades",
        CASE 
            WHEN flag_calculo_matriz_tempo_viagem = 'C' THEN 'CONCLUÍDO'
            ELSE 'FALHA'
        END AS "Cálculo da matriz de tempo",
        CASE 
            WHEN flag_calculo_indice_15min = 'C' THEN 'CONCLUÍDO'
            ELSE 'FALHA'
        END AS "Cálculo do indice"
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
            ( %(peso_p1)s * indice_p1 + indice_p2 *  %(peso_p2)s) / (  %(peso_p1)s +  %(peso_p2)s) AS indice
        FROM t_indice_unidade_federativa as i 
        INNER JOIN t_unidade_federativa as m 
        ON i.codigo_unidade_federativa = m.codigo
        )
        SELECT 
            regiao, 
            ST_AsText(ST_Simplify(ST_Union(geometria), 0.001)) as geometry, 
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
            municipio.codigo,
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
        WHERE matriz.tempo_viagem_seg <= 900
            AND municipio.codigo = %(municipio)s
            AND matriz.codigo_modalidade_transporte = %(modalidade)s
        GROUP BY categoria.nome, municipio.codigo
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

    HEXAGO_CALCULADOS_BRASIL= '''  
           WITH total_hexagonos AS (
                SELECT
                    'Total' AS descricao,
                    COUNT(0) AS quantidade
                FROM t_malha_hexagonal_municipio
            ),
            total_hexagonos_municipio_erro AS (
                SELECT
                    'Hexágonos de municípios com erro' AS descricao,
                    COUNT(0) AS quantidade
                FROM t_malha_hexagonal_municipio malha
                INNER JOIN t_municipio municipio
                    ON malha.codigo_municipio = municipio.codigo
                WHERE (
                    municipio.flag_extracao_amenidades = 'E' OR 
                    municipio.flag_calculo_matriz_tempo_viagem = 'E'
                )
            ),
            total_hexagonos_indice_calculado AS (
                SELECT
                    'Hexágonos com índice calculado' AS descricao,
                    COUNT(0) AS quantidade
                FROM t_indice_hexagono
                WHERE codigo_modalidade_transporte = %(modalidade)s
            ),
            total_hexagonos_sem_indice AS (
                SELECT
                    'Hexágonos sem índice' AS descricao,
                    (tot_hex.quantidade - tot_err.quantidade - tot_idx.quantidade) AS quantidade
                FROM 
                    total_hexagonos tot_hex, 
                    total_hexagonos_municipio_erro tot_err, 
                    total_hexagonos_indice_calculado tot_idx 
            )
            SELECT *
            FROM total_hexagonos_municipio_erro
            UNION
            SELECT *
            FROM total_hexagonos_indice_calculado
            UNION
            SELECT *
            FROM total_hexagonos_sem_indice
            '''
    BUSCA_QUANTIDADE_AMENIDADE_CATEGORIA = '''
        WITH amenidade_encontrada AS (
                SELECT  COUNT(codigo_categoria_pai) AS contagem, codigo_categoria_pai
                FROM t_amenidade_municipio m
                INNER JOIN t_feicao_osm tfo ON m.codigo_feicao_osm = tfo.codigo
                INNER JOIN t_categoria_amenidade tca ON tfo.codigo_categoria_amenidade = tca.codigo
                GROUP BY codigo_categoria_pai
            )

            SELECT
                contagem,
                am.codigo_categoria_pai,
                nome as categoria
            FROM amenidade_encontrada AS am
            INNER JOIN t_categoria_amenidade tca ON am.codigo_categoria_pai = tca.codigo;'''
            
    BUSCA_QUANTIDADE_AMENIDADE_CATEGORIA_ESTADO = '''
        WITH amenidade_encontrada AS (
                SELECT  COUNT(codigo_categoria_pai) AS contagem, codigo_categoria_pai
                FROM t_amenidade_municipio m
                INNER JOIN t_feicao_osm tfo ON m.codigo_feicao_osm = tfo.codigo
                INNER JOIN t_categoria_amenidade tca ON tfo.codigo_categoria_amenidade = tca.codigo
                INNER JOIN t_municipio as tm ON m.codigo_municipio=tm.codigo
                INNER JOIN t_unidade_federativa as uf ON uf.codigo =tm.codigo_unidade_federativa 
                WHERE uf.codigo = %(estado)s
                GROUP BY codigo_categoria_pai
            )
            SELECT
                contagem,
                am.codigo_categoria_pai,
                nome as categoria
            FROM amenidade_encontrada AS am
            INNER JOIN t_categoria_amenidade tcam ON am.codigo_categoria_pai = tcam.codigo;'''
            
    BUSCA_QUANTIDADE_AMENIDADE_CATEGORIA_MUNICIPIO = '''
        WITH amenidade_encontrada AS (
                SELECT  COUNT(codigo_categoria_pai) AS contagem, codigo_categoria_pai
                FROM t_amenidade_municipio m
                INNER JOIN t_feicao_osm tfo ON m.codigo_feicao_osm = tfo.codigo
                INNER JOIN t_categoria_amenidade tca ON tfo.codigo_categoria_amenidade = tca.codigo
                INNER JOIN t_municipio as tm ON m.codigo_municipio=tm.codigo
                WHERE tm.codigo = %(municipio)s
                GROUP BY codigo_categoria_pai
            )

            SELECT
                contagem,
                am.codigo_categoria_pai,
                nome as categoria
            FROM amenidade_encontrada AS am
            INNER JOIN t_categoria_amenidade tcam ON am.codigo_categoria_pai = tcam.codigo;'''
            
            
    AMENIDADE_POR_REGIAO = '''
            SELECT 
                unidade.regiao AS regiao, 
                categoria_pai.nome AS categoria,
                COUNT(0) AS quantidade
            FROM t_amenidade_municipio amenidade
            INNER JOIN t_feicao_osm feicao
                ON amenidade.codigo_feicao_osm = feicao.codigo
            INNER JOIN t_categoria_amenidade categoria
                ON feicao.codigo_categoria_amenidade = categoria.codigo
            INNER JOIN t_categoria_amenidade categoria_pai
                ON categoria.codigo_categoria_pai = categoria_pai.codigo
            INNER JOIN t_municipio municipio	
                ON amenidade.codigo_municipio = municipio.codigo
            INNER JOIN t_unidade_federativa unidade
                ON municipio.codigo_unidade_federativa = unidade.codigo
            GROUP BY
                categoria_pai.codigo,
                categoria_pai.nome,
                unidade.regiao
            ORDER BY
                unidade.regiao,
                categoria_pai.codigo;'''