from dash import html, dcc, dash
from components.mapa import Mapa
import dash_bootstrap_components as dbc
from components.tabela import TabelaEtapas
from components.histograma import Histrograma
from components.grafico_rosca import GraficoRosca
from components.grafico_barras import GraficoBarra
from dash.dependencies import Input, Output, State
from components.subplot_regiao import SubPlotRegiao
from components.card_amenidade import CardAmenidades
from components.formulario.form import cria_formulario
from components.grafico_dispercao import GraficoDispersao

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

server = app.server
app.scripts.config.serve_locally = True
server = app.server

mapa = Mapa()
histograma = Histrograma()
grafico_rosca = GraficoRosca()
tabela_etapas = TabelaEtapas()
grafico_barra = GraficoBarra()
card_amenidades = CardAmenidades()
grafico_dispersao = GraficoDispersao()
subplot = SubPlotRegiao()


def constroi_card_amenidade(amenidade):
    return dbc.CardBody([html.Div([html.H1(amenidade['quantidade_amenidade'].iloc[0], className="card_body_big_number"),
                            html.P(amenidade['titulo'].iloc[0], className="card_body_big_number_texto")],)
                         ],)
    
def constroi_componente_md_4(grafico, id):
    return dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(figure=grafico, id=id)), className='card'), md=4, className="graficos")

def constroi_componente_md_6(grafico, id):
    return dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(figure=grafico, id=id)), className='card'), md=6, className="graficos")

def constroi_componente_md_8(grafico, id):
    return dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id=id, figure=grafico)), className='card'), md=8, className="graficos")

def constroi_componente_md_12(grafico, id):
    return dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id=id, figure=grafico)), className='card'), md=12, className="graficos")




formulario = html.Div(cria_formulario(), id='modal_formulario')
mapa_brasil_fig = dbc.Row([dcc.Graph(id="map_brasil", figure=mapa.constroi_mapa_brasil())])
mapa_subplot = constroi_componente_md_12(subplot.constroi_subplot_brasil(), id='subplot')
card_histograma = constroi_componente_md_12(grafico=histograma.constroi_histograma_brasil(modalidade=1), id='histograma')
card_grafico_menor = constroi_componente_md_6(grafico=grafico_barra.controi_grafico_brasil_menor_indice(), id='grafico_menor')
card_grafico_maior = constroi_componente_md_6(grafico=grafico_barra.controi_grafico_brasil_maior_indice(),  id='grafico_maior')
card_grafico_dispersao = constroi_componente_md_12(grafico_dispersao.constroi_grafico_dispersao_brasil(), id='dispersao')
amenidade_por_regiao = constroi_componente_md_12(grafico_barra.controi_grafico_amenidade_por_regiao(), id='amenidade')
card_rosca_hexagonos = constroi_componente_md_4(grafico=grafico_rosca.controi_quantidade_hexagono_analisados_brasil(), id='grafico_rosca_hexagono')
card_histograma_categoria_amenidade = constroi_componente_md_8(histograma.constroi_histograma_quantidade_amenidades_brasil(), id='histograma_amenidade')
(quantidade_amenidade_brasil, 
maior_quantidade_amenidade_brasil,
menor_quantidade_amenidade_brasil) = card_amenidades.constroi_amenidades_brasil()




app.layout = dbc.Container(
        children=[
                dbc.Row([
                    dbc.Col([formulario], md=3, id="form"),
                    dbc.Col([dcc.Loading(mapa_brasil_fig)], md=9),
                ]),                          
                dbc.Row([
                    dbc.Col(
                        dcc.Loading(children=dbc.Card(children=constroi_card_amenidade(quantidade_amenidade_brasil), 
                                 body=True, id="card_amenidade_total", className="card_amenidade")), 
                        className="amenidade", width=4),
                    dbc.Col(
                        dcc.Loading(dbc.Card(children=constroi_card_amenidade(maior_quantidade_amenidade_brasil), 
                                 body=True, id="card_amenidade_maior", className="card_amenidade")),
                        className="amenidade", width=4),
                    dbc.Col(
                        dcc.Loading(dbc.Card(children=constroi_card_amenidade(menor_quantidade_amenidade_brasil),
                                 body=True, id="card_amenidade_menor", className="card_amenidade")), 
                        className="amenidade", width=4),
                ]),
                dbc.Row([card_grafico_dispersao], id='tab'),  
                dbc.Row([card_grafico_maior,card_grafico_menor], id='graficos'),
                dbc.Row(card_histograma ),
                dbc.Row([card_histograma_categoria_amenidade, card_rosca_hexagonos], id='graficos_inferior'),
                dbc.Row(dcc.Loading(mapa_subplot), id='mapa_subplot'),
                dbc.Row(dcc.Loading(amenidade_por_regiao), id='amenidade_regiao'),
                
        ], fluid=True, id="container")


@app.callback(
    Output('map_brasil', 'figure'),
    [State('estado-dropdown', 'value'), 
    State('indice_valores', 'value'), 
    State('municipio-dropdown', 'value'),     
    State('indice_amenidade', 'value'),
    State('indice_variedade_amenidade', 'value'), 
    State('modalidade-transporte', 'value'),
    Input('button','n_clicks'),]
)
def atualiza_mapa(estado, indice, municipio, peso_p1, peso_p2, modalidade, filtrar):
    if municipio is not None:
        return mapa.constroi_mapa_municipio(municipio=municipio,
                                         modalidade=modalidade, 
                                         indice_min=indice[0], 
                                         indice_max=indice[1],
                                         peso_p1=peso_p1, 
                                         peso_p2=peso_p2)
    if estado is not None:
        return mapa.constroi_mapa_estado(estado=estado,
                                         modalidade=modalidade, 
                                         indice_min=indice[0], 
                                         indice_max=indice[1],
                                         peso_p1=peso_p1, 
                                         peso_p2=peso_p2)
    
    return mapa.constroi_mapa_brasil(modalidade=modalidade, 
                                         indice_min=indice[0], 
                                         indice_max=indice[1],
                                         peso_p1=peso_p1, 
                                         peso_p2=peso_p2)
    

@app.callback(
    [Output('graficos', 'children'),
    Output('histograma', 'figure'),
     Output('mapa_subplot', 'children')],
    [State('estado-dropdown', 'value'), 
     State('municipio-dropdown', 'value'),
     State('indice_valores', 'value'),
     State('indice_amenidade', 'value'),
     State('indice_variedade_amenidade', 'value'),  
     State('modalidade-transporte', 'value'),
     Input('button','n_clicks'),
]
)
def update_grafico(estado, municipio, indice, peso_p1, p2_peso, modalidade, filtrar):
    if municipio is not None:
        return [dbc.Col()], histograma.constroi_histograma_municipio(modalidade=modalidade, municipio=municipio), dbc.Col()
    if estado is not None:     
        g_estado_maior = grafico_barra.controi_grafico_estado_maior_indice(modalidade=modalidade, 
                                                                           peso_p1=peso_p1,
                                                                           estado=estado, 
                                                                           peso_p2=p2_peso,
                                                                           indice_min=indice[0],
                                                                           indice_max=indice[1])
        
        g_estado_menor = grafico_barra.controi_grafico_estado_menor_indice(modalidade=modalidade, 
                                                                           peso_p1=peso_p1,
                                                                           estado=estado, 
                                                                           peso_p2=p2_peso, 
                                                                           indice_min=indice[0],
                                                                           indice_max=indice[1])
        histograma_amenidade  = histograma.constroi_histograma_estado(estado=estado, modalidade=modalidade)
        return [constroi_componente_md_6(g_estado_maior, id='grafico_maior'), constroi_componente_md_6(g_estado_menor, id='grafico_menor')], histograma_amenidade, dbc.Col()
    
    g_brasil_maior = grafico_barra.controi_grafico_brasil_maior_indice(modalidade=modalidade, 
                                                                       peso_p1=peso_p1,
                                                                       peso_p2=p2_peso,
                                                                       indice_min=indice[0],
                                                                       indice_max=indice[1])
    
    g_brasil_menor = grafico_barra.controi_grafico_brasil_menor_indice(modalidade=modalidade,
                                                                       peso_p1=peso_p1, 
                                                                       peso_p2=p2_peso, 
                                                                       indice_min=indice[0],
                                                                       indice_max=indice[1])
    
    histograma_amenidade = histograma.constroi_histograma_brasil(modalidade=modalidade)
    
    subplot_brasil  = constroi_componente_md_12(subplot.constroi_subplot_brasil(modalidade=modalidade, peso_p1=peso_p1, peso_p2=p2_peso), id='subplot')
    return [constroi_componente_md_6(g_brasil_maior, id='grafico_maior'), constroi_componente_md_6(g_brasil_menor,  id='grafico_menor')], histograma_amenidade, subplot_brasil
    

@app.callback(
    [Output('card_amenidade_total', 'children'),
    Output('card_amenidade_maior', 'children'),
    Output('card_amenidade_menor', 'children')],
    [State('estado-dropdown', 'value'), 
     State('municipio-dropdown', 'value'),
     Input('button', 'n_clicks'),
    ]
)
def update_cards_amenidade(estado, municipio, filtrar):
    
    if municipio is not None:
        (quantidade_amenidade_municipio,
         quantidade_amenidade_mais_comum_municipio, 
         quantidade_amenidademenos_comum_municipio) = card_amenidades.amenidades_municipio(municipio=municipio)
        
        return (constroi_card_amenidade(quantidade_amenidade_municipio), 
                constroi_card_amenidade(quantidade_amenidade_mais_comum_municipio), 
                constroi_card_amenidade(quantidade_amenidademenos_comum_municipio))
    if estado is not None:     
        (quantidade_amenidade_estado,
         quantidade_amenidade_mais_comum_estado,
         quantidade_amenidade_menos_comum_estado) = card_amenidades.constroi_amenidades_estado(estado=estado)
        
        return (constroi_card_amenidade(quantidade_amenidade_estado), 
                constroi_card_amenidade(quantidade_amenidade_mais_comum_estado), 
                constroi_card_amenidade(quantidade_amenidade_menos_comum_estado))
    
    (quantidade_amenidade_brasil, 
    maior_quantidade_amenidade_brasil,
    menor_quantidade_amenidade_brasil) = card_amenidades.constroi_amenidades_brasil()   
    
    return (constroi_card_amenidade(quantidade_amenidade_brasil), 
            constroi_card_amenidade(maior_quantidade_amenidade_brasil), 
            constroi_card_amenidade(menor_quantidade_amenidade_brasil))

@app.callback( 
    Output('tab', 'children'),
    [State('estado-dropdown', 'value'), 
     State('municipio-dropdown', 'value'),
     State('indice_valores', 'value'),
     State('indice_amenidade', 'value'),
     State('indice_variedade_amenidade', 'value'),  
     State('modalidade-transporte', 'value'),
     Input('button','n_clicks'),
]
)
def atualiza_tabela_grafico(estado, municipio, indice, peso_p1, peso_p2, modalidade, filtrar):
    if municipio is not None:
        return None
    if estado is not None:      
        return [constroi_componente_md_8(tabela_etapas.constroi_tabela_municipio(estado=estado), id='tabela'), 
                constroi_componente_md_4(grafico=grafico_rosca.controi_municipio_analisados(estado=estado), id='grafico_rosca')]
        
    return constroi_componente_md_12(grafico_dispersao.constroi_grafico_dispersao_brasil(modalidade=modalidade,
                                                     indice_min=indice[0],
                                                     indice_max=indice[1],
                                                     peso_p1=peso_p1, 
                                                     peso_p2=peso_p2), id='grafico_dispersao')
    

@app.callback( 
    Output('graficos_inferior', 'children'),
    Output('amenidade_regiao', 'children'),
    [State('estado-dropdown', 'value'), 
     State('municipio-dropdown', 'value'),
     State('indice_valores', 'value'),
     State('indice_amenidade', 'value'), 
     State('indice_variedade_amenidade', 'value'),  
     State('modalidade-transporte', 'value'),
     Input('button','n_clicks'),
]
)
def atualiza_histograma_pizza(estado, municipio, indice, peso_p1, peso_p2, modalidade, filtrar):
    if municipio is not None:
        card_histograma_categoria_amenidade = constroi_componente_md_12(histograma.constroi_histograma_quantidade_amenidades_municipio(municipio), id='histograma_amenidade')
        #card_rosca_hexagonos = constroi_componente_grafico_rosca(grafico=grafico_rosca.controi_quantidade_hexagono_analisados_municipio(municipio), id='grafico_rosca_hexagono')
        return [card_histograma_categoria_amenidade], dbc.Col()
    if estado is not None:     
        card_histograma_categoria_amenidade = constroi_componente_md_12(histograma.constroi_histograma_quantidade_amenidades_estado(estado), id='histograma_amenidade')
        #card_rosca_hexagonos = constroi_componente_grafico_rosca(grafico=grafico_rosca.controi_quantidade_hexagono_analisados_estado(estado), id='grafico_rosca_hexagono')
        return [card_histograma_categoria_amenidade], dbc.Col()
    
    card_rosca_hexagonos = constroi_componente_md_4(grafico=grafico_rosca.controi_quantidade_hexagono_analisados_brasil(), id='grafico_rosca_hexagono')
    card_histograma_categoria_amenidade = constroi_componente_md_8(histograma.constroi_histograma_quantidade_amenidades_brasil(), id='histograma_amenidade')


    return [card_histograma_categoria_amenidade, card_rosca_hexagonos], [amenidade_por_regiao]


if __name__ == '__main__':
    app.run_server(host="localhost", port="8080")
