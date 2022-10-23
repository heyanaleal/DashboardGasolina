import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO


# ========= App ============== #
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc_css])
app.scripts.config.serve_locally = True
server = app.server

# ========== Styles ============ #

template_theme1 = "flatly"
template_theme2 = "vapor"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.VAPOR
tab_card = {'height': '100%'}


# ===== Reading n cleaning File ====== #
df_main = pd.read_csv("GasPrices-Dash\data_gas.csv")


df_main.info()
# PASSAR PARA DATE TIME
df_main['DATA INICIAL'] = pd.to_datetime(df_main["DATA INICIAL"])
df_main['DATA FINAL'] = pd.to_datetime(df_main['DATA FINAL'])
#CALCULAR A MÉDIA 
df_main['DATA MEDIA'] =((df_main['DATA FINAL']- df_main['DATA INICIAL'])/2) + df_main['DATA INICIAL']
#ORDENAR PELA MÉDIA 
df_main= df_main.sort_values(by='DATA MEDIA',ascending = True )
# RENOMEAR COLUNAS
df_main.rename(columns = {'DATA MEDIA': 'DATA'}, inplace=True)
df_main.rename(columns = {'PREÇO MÉDIO REVENDA': 'VALOR REVENDA (R$/L)'},inplace= True)

#CRIANDO COLUNA DE ANO 
df_main["ANO"]= df_main["DATA"].apply(lambda x: str (x.year))
#PEGAR APENAS OS DADOS DA GASOLINA 
df_main = df_main [df_main.PRODUTO == "GASOLINA COMUM"]

# RESET DATAFRAME
df_main = df_main.reset_index()

# EXCLUINDO COLUNAS 
df_main.drop(['UNIDADE DE MEDIDA', 'COEF DE VARIAÇÃO REVENDA', 'COEF DE VARIAÇÃO DISTRIBUIÇÃO', 
    'NÚMERO DE POSTOS PESQUISADOS', 'DATA INICIAL', 'DATA FINAL', 'PREÇO MÁXIMO DISTRIBUIÇÃO', 'PREÇO MÍNIMO DISTRIBUIÇÃO', 
    'DESVIO PADRÃO DISTRIBUIÇÃO', 'MARGEM MÉDIA REVENDA', 'PREÇO MÍNIMO REVENDA', 'PREÇO MÁXIMO REVENDA', 'DESVIO PADRÃO REVENDA', 
    'PRODUTO', 'PREÇO MÉDIO DISTRIBUIÇÃO'], inplace=True, axis=1)

# Para salvar no dcc.store
df_store = df_main.to_dict()

# =========  Layout  =========== #
app.layout = dbc.Container(children=[

 dcc.Store(id='dataset',data = df_store),
 dcc.Store(id='dataset_fixed', data= df_store),

 #LAYOUT
 #ROW
 dbc.Row([
    dbc.Col([
       dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                 html.Legend("DashBoard Gasolina")
                ],sm = 8),
                dbc.Col([
                    html.I(className ='fa fa-filter', style = {'font-size' : '300%'})
                ],sm=4, align ="center")
            ]),
            dbc.Row([
                dbc.Col([
                    ThemeSwitchAIO(aio_id='theme', themes = [url_theme1, url_theme2]),
               #  html.I(className = 'fa-square-github', style = {'font-size' : '300%'}),
                    html.Legend("GitHub")
                ])
            ], style = {'margin-top': '10px'}),
            dbc.Row([
                dbc.Col(
                    dbc.Button("Visite o GitHub", href="https://github.com/heyanaleal", target="_blank")
                )
            ], style = {'margin-top': '10px'})
        ])
       ], style = tab_card) 
    ], sm = 4, lg=2),
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H3('Máximo e Mínimos'),
                        dcc.Graph(id='static-maxnin', config={"displayModeBar": False , "showTips":False})
                    ])
                ])
            ])
        ], style = tab_card)
    ], sm=8, lg=3),
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6('Ano de análise:'),
                        dcc.Dropdown(
                            id="select_ano",
                            value=df_main.at[df_main.index[1],'ANO'],
                            clearable=False,
                            className='dbc',
                            options=[
                                {"label": x, "value": x} for x in df_main.ANO.unique()
                            ]),
                    ],sm=6),
                ])
            ])
        ])
    ])
 ])




], fluid=True, style={'height': '100%'})


# ======== Callbacks ========== #


# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
