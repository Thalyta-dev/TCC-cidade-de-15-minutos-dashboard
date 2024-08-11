from dash import html, dcc, dash
from components.mapa import Mapa
import dash_bootstrap_components as dbc
from components.tabela import TabelaEtapas
from components.histograma import Histrograma
from components.grafico_rosca import GraficoRosca
from components.grafico_barras import GraficoBarra
from dash.dependencies import Input, Output, State
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


def constroi_card_amenidade(amenidade):
    return dbc.CardBody([html.Div([html.H1(amenidade['quantidade_amenidade'].iloc[0], className="card_body_big_number"),
                            html.P(amenidade['titulo'].iloc[0], className="card_body_big_number_texto")],)
                         ],)
def constroi_componente_grafico_barra(grafico):
    return dbc.Col(dbc.Card(dcc.Graph(figure=grafico)), md=6, className="graficos")

def constroi_componente_histograma(histograma):
    return dbc.Col(dbc.Card(dcc.Graph(id='histograma', figure=histograma)), md=12, className="graficos")

def constroi_componente_grafico_rosca(grafico):
    return dbc.Col(dbc.Card(dcc.Graph(id="grafico_rosca_estado", figure=grafico), body=True), 
                   width=4, className="graficos")

def constroi_componente_tabela(tabela):
    return dbc.Col(dbc.Card(dcc.Graph(id="tabela_erros_etapa", figure=tabela),  body=True),
                   width=8, className="graficos")

def constroi_componente_grafico_dispersao(grafico_dispersao):
    return dbc.Col(dbc.Card(dcc.Graph(figure=grafico_dispersao),  body=True),
                   width=12, className="graficos")


formulario = cria_formulario()
mapa_brasil_fig = dbc.Row([dcc.Graph(id="map_brasil", figure=mapa.constroi_mapa_brasil())])
card_histograma = constroi_componente_histograma(histograma=histograma.constroi_histograma_brasil(modalidade=1))
card_grafico_menor = constroi_componente_grafico_barra(grafico=grafico_barra.controi_grafico_brasil_menor_indice())
card_grafico_maior = constroi_componente_grafico_barra(grafico=grafico_barra.controi_grafico_brasil_maior_indice())
card_grafico_dispersao = constroi_componente_grafico_dispersao(grafico_dispersao.constroi_grafico_dispersao_brasil())
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
                        dbc.Card(children=constroi_card_amenidade(quantidade_amenidade_brasil), 
                                 body=True, id="card_amenidade_total", className="card_amenidade"), 
                        className="amenidade", width=4),
                    dbc.Col(
                        dbc.Card(children=constroi_card_amenidade(maior_quantidade_amenidade_brasil), 
                                 body=True, id="card_amenidade_maior", className="card_amenidade"),
                        className="amenidade", width=4),
                    dbc.Col(
                        dbc.Card(children=constroi_card_amenidade(menor_quantidade_amenidade_brasil),
                                 body=True, id="card_amenidade_menor", className="card_amenidade"), 
                        className="amenidade", width=4),
                ]),
                dbc.Row([card_grafico_dispersao], id='tab' ),
                dbc.Row([card_grafico_maior,card_grafico_menor], id='graficos'),
                dbc.Row(card_histograma)
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
    Output('histograma', 'figure')],
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
        return [dbc.Col()], histograma.constroi_histograma_municipio(modalidade=modalidade, municipio=municipio)
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
        return [constroi_componente_grafico_barra(g_estado_maior), constroi_componente_grafico_barra(g_estado_menor)], histograma_amenidade
    
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
    
    return [constroi_componente_grafico_barra(g_brasil_maior), constroi_componente_grafico_barra(g_brasil_menor)], histograma_amenidade
    

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
        return [constroi_componente_tabela(tabela=tabela_etapas.constroi_tabela_municipio(estado=estado)), 
                constroi_componente_grafico_rosca(grafico=grafico_rosca.constroi_grafico_rosca_estado(estado=estado))]
        
    return constroi_componente_grafico_dispersao(grafico_dispersao.constroi_grafico_dispersao_brasil(modalidade=modalidade,
                                                     indice_min=indice[0],
                                                     indice_max=indice[1],
                                                     peso_p1=peso_p1, 
                                                     peso_p2=peso_p2))
    

if __name__ == '__main__':
    app.run_server(host="localhost", port="8050")
