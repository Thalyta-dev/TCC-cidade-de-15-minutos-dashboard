
from utils.form_util import FormUtil
from dash import html, dcc
import dash_bootstrap_components as dbc

titulo = "15MinCityInfo"
texto_explicativo = """ Exploração dos índices de estados e municípios com o conceito de 'cidade de 15 minutos."""

select_estado = dcc.Dropdown(
                    id="estado-dropdown",
                    options=[{"label": i, "value": j} for i, j in FormUtil.dic_estados().items()],
                    value=None,
                    placeholder="Selecione o estado")

select_municipio = dcc.Dropdown(
                    id="municipio-dropdown",
                    value=None,
                    options= [{"label": nome, "value": codigo} for nome, codigo in FormUtil.dic_municipios().items()],
                    placeholder="Selecione o município"
                )

select_indice = dcc.RangeSlider(
                    min=0, 
                    max=100, 
                    step=20, 
                    className="form_elemento",
                    id='indice_valores', 
                    value=[0, 100],
                    marks = {i: str(i) for i in FormUtil.array_indice()})

select_modalidade = dcc.RadioItems(
                        id='modalidade-transporte',
                        value=1,
                        options=[
                            {'label': '  Caminhada', 'value': '1'},
                            {'label': '  Bicicleta', 'value': '2'}
                        ],
                        labelStyle={'display': 'inline-block', 'margin-right': '20px'}
                    )

select_indice_amenidade = dcc.Input(
                        id="indice_amenidade",
                        type= "number",
                        min=0,
                        value=1,  
                        max=100, 
                        placeholder="Digite um numero de 0 a 100",
                    )
    
select_indice_variedade_amenidade = dcc.Input(
                        id="indice_variedade_amenidade",
                        type= "number",
                        min=0,
                        value=1,  
                        max=100, 
                        placeholder="Digite um numero de 0 a 100",
                    )


def cria_formulario():  
    return dbc.Row([
                dcc.Store(id='store-global'),
                dbc.Col(html.Div(html.Div(titulo, id="titulo_cabecalho")),id="cabecalho"),
                
                html.P(texto_explicativo),
                
                html.H4("""Estados"""),
                select_estado,

                html.H4("""Municípios"""),
                select_municipio, 
                
                html.H4("""Peso amenidades"""),
                select_indice_amenidade,
                
                html.H4("""Peso variedade de amenidades"""),
                select_indice_variedade_amenidade,
                
                html.H4("""Modalidade Transporte"""),
                select_modalidade,

                html.H4("""Índice"""),
                select_indice,
                
                html.Button('Filtrar', id='button', className="form_elemento", n_clicks=0)
            ])




