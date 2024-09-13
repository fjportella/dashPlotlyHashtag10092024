
#- Layouts
#    - HTML - Tudo que estiver visualizando - Layout, textos, imagens
#    - Dash Components (Core Components)  = São os componentes do dashboard - gráficos, legenda, botões
#- CALLBACKS = Tudas as funcionalidades dinâmicas, ou seja é a logica que comanda a dinâmica.

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

#Criando Aplicativo Dash (inicializando variável app com o Dash)
app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

#Importando planilha para o dataframe
df = pd.read_excel("Vendas2.xlsx")

lista_marcas = list(df["Marca"].unique())
lista_marcas.append("Todas")

lista_paises = list(df["País"].unique())
lista_paises.append("Todos")

#Cria o Gráfico de acordo com o plotly
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
fig2 = px.scatter(df, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)

#Layout da Página
#Todo html tem o elemento children
#Pode usar também CSS para por exemplo alinhar centralizado. 
# Pode ser aplicado para cada itens ou para todos colocando o css no final do código
app.layout = html.Div(children=[
    html.H1(children='Meu Dashboard'),

    html.Div(children='''
        Dashboard de vendas em Python.
    ''', style={"text-align":"left"}),

    html.H3(children = "Vendas de cada produto por Loja", id="subtitulo"),

    #Criando botão radio.
    #Recebe: Lista de Opções, Valor e ID
    #inline coloca os radios em uma mesma linha
    #Value recebe o valor padrão para o carregamento da página, por exemplo Todas
    dcc.RadioItems(lista_marcas, value="Todas", id='selecao_marcas', inline=True),
    #colocando o dropdown dentro de uma div para editar css
    html.Div(children=[
    dcc.Dropdown(options=lista_paises, value="Todos", id='selecao_pais'), # "options=" é opcional, pois pode passar ou não
    ], style={"width": "50%", "margin": "auto"}),

    #Plotando os Gráficos
    dcc.Graph(id='vendas_por_loja', figure=fig),
    dcc.Graph(id='distribuicao_vendas', figure=fig2),

    

], style={"text-align":"center"})


#esse callback é para filtrar os países, de acordo com os radios, para não exibir país que não tenha valor
@app.callback(
    Output('selecao_pais', 'options'), #id, parametro. Edita parametro options do dropdown
    Input('selecao_marcas', 'value'), #id, parametro
)
def opcoes_pais(marca):
    #quais países ele irá pegar
    if marca == "Todas":
        nova_lista_paises = list(df["País"].unique())
        nova_lista_paises.append("Todos")
    else:
        df_filtrada = df.loc[df['Marca']==marca, :]
        nova_lista_paises = list(df_filtrada["País"].unique())
        nova_lista_paises.append("Todos")
    return nova_lista_paises #retorna a lista de países do option


#Callbacks para editar botões de filtro
#É o que dá funcionalidade para os botões. É o que conecta os botões com o gráfico
#Output = Quem eu quero que o botão do Input modifique. Ex: id = subtitulo e valor = children
#Input = Quem está modificando os gráficos (ex: radio). De onde eu quero pegar as informações, que está fazendo o filtro
#Input Ex: id = selecao_marcas e valor = value
#no def será indicado uma variável qualquer, no exemplo = marca. e depois a lógica da mudança do texto
#Pode não parecer que não estamos usando o função selecionar_marca, mas o callback por baixo dos panos a utiliza
#Primeiro todos Output e depois o Input. e No return precisa ser a mesma ordem do Output
#se tiver 2 ou mais botões editando todos gráficos, passamos os inputs no mesmo callback
#se 2 botões estiverem editando gráficos diferentes, criamos outro callback
@app.callback(
    Output('subtitulo', 'children'),
    Output('vendas_por_loja', 'figure'),
    Output('distribuicao_vendas', 'figure'),
    Input('selecao_marcas', 'value'),
    Input('selecao_pais', 'value'), 
)
def selecionar_marca(marca, pais): #o parametro marca é o valor que vem do input
    if marca == "Todas" and pais == "Todos":
        texto = f"Vendas de Cada Produto por Loja"
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig2 = px.scatter(df, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)
    else:
        #filtra as linhas da tabela onde a variável marca é igual a treinamentos ou programação
        #podemos usar loc do pandas. neste caso, passamos linha (usando Marca) e todas as colunas (:)
        #para dois ou mais filtros, criar copia do df e  if para identificar os filtros
        df_filtrado = df
        if marca != "Todas":
            df_filtrado = df_filtrado.loc[df_filtrado['Marca']==marca, :]
        if pais != "Todos":
            df_filtrado = df_filtrado.loc[df_filtrado['País']==pais, :]
        texto = f"Vendas de Cada Produto por Loja da marca {marca} e do País {pais}"
        fig = px.bar(df_filtrado, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig2 = px.scatter(df_filtrado, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)

    return texto, fig, fig2 #retorno dos outputs


if __name__ == '__main__':
    app.run(debug=True)