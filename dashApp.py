import dash 
from dash import dcc;
from dash import html;
from dash import Input;
from dash import Output;
from dash import callback;
import pandas as pd;
import plotly.express as px;

df = pd.read_csv("vendas_mes.csv");


df['Faturamento'] = df['Preco_Unitario'] * df['Quantidade'];

df['Data_Venda'] = pd.to_datetime(df['Data_Venda']);


optionsCat = [{'label': 'Todos', 'value': 'Todos'}];
for categoria in df['Categoria'].unique():
    optionsCat.append({'label': categoria, 'value': categoria});


#tailwind = "https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4";

app = dash.Dash(__name__);

styleCard = {
    'textAlign': 'center', 'padding': '20px', 'margin': '10px',
    'border': '1px solid #ddd', 'borderRadius': '5px',
    'backgroundColor': '#f9f9f9', 'flex': 1
}

app.layout = html.Div(children=[

    html.Div(children=[
        html.H1(children='Dashboard de Perfomace de Vendas', style={'margin': '0', 'marginTop': '10px'}),

        html.P(children='Análise de faturamento e volume de vendas do último mês.')
        ], style={'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'alignItems': 'center'}),
    
    html.Hr(),

    html.Div(children=[
        html.Div(children=[
            html.Label('Filtro-Categoria'),
            dcc.Dropdown(
                id='Filtro-Categoria',
                options=optionsCat,
                value='Todos',
                clearable=False,
                style={'width': '100%'}
            )
            ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px', 'justifyContent': 'center', 'alignItems': 'center', 'width': '49%', 'flex': '0 0 calc(49% - 10px)'}),
        
        html.Div(children=[
            html.Label('Filtro por Data:'),
            dcc.DatePickerRange(
                id='seletor-datas',
                min_date_allowed=df['Data_Venda'].min().date(),
                max_date_allowed=df['Data_Venda'].max().date(),
                start_date=df['Data_Venda'].min().date(),
                end_date=df['Data_Venda'].max().date(),
                display_format='DD/MM/YYYY',
            ), 
            ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px', 'width': '49%', 'justifyContent': 'center', 'alignItems': 'center', 'flex': '0 0 calc(49% - 10px)'})

        ], style={'display': 'flex','padding': '10px', 'gap': '10px', 'width': '100%', 'justifyContent': 'center', 'alignItems': 'center', 'flexWrap': 'wrap'}),
    
    html.Hr(),

        html.Div(children=[
            html.Div(style=styleCard, children=[
                html.H3('Faturamento Total'),
                html.H2(id='card-Faturamento', children='R$ 0.00')
            ]),

            html.Div(style=styleCard, children=[
                html.H3('Itens vendidos'),
                html.H2(id='card-itens', children='0')
            ]),

            html.Div(style=styleCard, children=[
                html.H3('Preco Médio por item'),
                html.H2(id='card-precoMedio', children='R$ 0.00')
            ])
            
        ], style={'width': '100%', 'display': 'flex'}),

    html.Hr(),
    
    html.Div(children=[
        dcc.Graph(
            id="GraficoVendasDias"
        ),

        dcc.Graph(
            id="graficoFaturamento", 
        ),
    ], style={'display': 'flex', 'gap': '10px', 'flexDirection': 'column'})
    
    
    ], style={'fontFamily': 'Arial, sans-serif', 'overflowX': 'hidden'});

@callback(
    Output('GraficoVendasDias', 'figure'),
    Output('graficoFaturamento', 'figure'),
    Output('card-Faturamento', 'children'),
    Output('card-itens', 'children'),
    Output('card-precoMedio', 'children'),
    [
        Input('Filtro-Categoria', 'value'),
        Input('seletor-datas', 'start_date'),
        Input('seletor-datas', 'end_date')
    ]
)

def atualizarGraficos(categoria, dataInicio, dataFim):
    if categoria == 'Todos':
        df_filtrado = df;
    else:
        df_filtrado = df[df['Categoria'] == categoria]; 
   
    data_inicio = pd.to_datetime(dataInicio);
    data_fim = pd.to_datetime(dataFim);

    df_filtrado = df_filtrado[(df_filtrado['Data_Venda'] >= data_inicio) & (df['Data_Venda'] <= data_fim)];

    QuantidadeDia = df_filtrado.groupby('Data_Venda', as_index=False)['Quantidade'].sum();

    faturamentoCategoria = df_filtrado.groupby('Categoria')['Faturamento'].sum().reset_index();

    faturamentoFiltrado = f"R$ {df_filtrado['Faturamento'].sum():.2f}"

    QuantidadeFiltrada = df_filtrado['Quantidade'].sum()

    precoMedio = f"R$ {(df_filtrado['Faturamento'].sum()) / (df_filtrado['Quantidade'].sum()):.2f}"

    


    grfLinha = px.line(
        QuantidadeDia,
        x='Data_Venda',
        y='Quantidade',
        title=f'Vendas Diarias para: {categoria}',
        labels={'Data_Venda': 'Data'},
        markers=True
    );

    grfBarra = px.bar(
        faturamentoCategoria,
        x='Categoria',
        y='Faturamento',
        title="Faturamento por Categoria",
        labels={'Faturamento': 'Faturamento (R$)'}
    );
    



    return grfLinha, grfBarra, faturamentoFiltrado, QuantidadeFiltrada, precoMedio ;

if __name__ == '__main__' :
    app.run(debug=True)
