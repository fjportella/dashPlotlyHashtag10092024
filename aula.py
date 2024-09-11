# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

#criando o aplicativo do flask
app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#dataframe (base de dados)
df = pd.read_excel("Vendas.xlsx")

#criando o gráfico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
opcoes = list(df['ID Loja'].unique())
opcoes.append("Todas as Lojas")

#layout da página
#construindo usando itens html (coisas relacionadas à página html)
#essa primeira linha é o html principal, onde engloba toda página (app.layout = html.Div)
app.layout = html.Div(children=[
    html.H1(children='Faturamento das Lojas'),
    html.H2(children='Gráfico com o Faturamento de Todos os Produtos Separados por Loja'),

    html.Div(children='''
        Obs: Esse gráfico mostra a quantidade de produtos vendidos, não o faturamento.
    '''),

    #componente botão dropdown
    dcc.Dropdown(opcoes, value='Todas as Lojas', id='lista_lojas'),

    #construindo usando itens dashboard (coisas relacionados ao dashboard)
    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
    )
])

#todos callback devem ficar aqui embaixo antes da chamada da página
@app.callback(    
    Output('grafico_quantidade_vendas', 'figure'), #quem será modificado/editado.
    Input('lista_lojas', 'value') #quem é que está trazendo os valores/informações a serem editados
)
def update_output(value):
    if value == "Todas as Lojas":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja']==value, :] #linha, coluna filtradas
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig


#serve para colocar no ar o site
if __name__ == '__main__':
    app.run(debug=True)
