# Para que a integração das páginas funcione, é necessário criar uma pasta com o nome 'pages' no mesmo diretório que este arquivo.

#Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import re
from datetime import datetime as dt, date, time

#Bibliotecas necessárias
import pandas as pd
import streamlit as st
import numpy as np
import folium
import inflection
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from PIL import Image

#========================================
#Funções
#========================================
def clean_code(df1):
    #Renomeando as colunas trocando ' ' por '_', aplicando lowcase e removendo espaços: 
    def rename_columns(dataframe):
        df = dataframe.copy()
        title = lambda x: inflection.titleize(x)
        snakecase = lambda x: inflection.underscore(x)
        spaces = lambda x: x.replace(" ", "")
        cols_old = list(df.columns)
        cols_old = list(map(title, cols_old))
        cols_old = list(map(spaces, cols_old))
        cols_new = list(map(snakecase, cols_old))
        df.columns = cols_new
        return df
    
    df1 = rename_columns(df1)
    
    #Criação dos nomes dos países:
    COUNTRIES = {
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America",
    }
    def country_name(country_id):
        return COUNTRIES[country_id]
    
    #Criando a coluna 'country_name' com os nomes dos países:
    df1['country_name']=df1['country_code'].apply(lambda x: country_name(x))
    
    
    #Criação do Tipo de Categoria de Comida:
    def create_price_tye(price_range):
        if price_range == 1:
            return "cheap"
        elif price_range == 2:
            return "normal"
        elif price_range == 3:
            return "expensive"
        else:
            return "gourmet"
    
    #Criação do nome das Cores:
    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
    }
    def color_name(color_code):
        return COLORS[color_code]

    #Criando a coluna 'country_name' com os nomes dos países:
    df1['color_name']=df1['rating_color'].apply(lambda x: color_name(x))
    
    #Removendo linha duplicadas
    df1 = df1.drop_duplicates().reset_index(drop=True)
    
    # Remover restaurantes com culinária 'NaN' e listar apenas o primeiro tipo de culinária da lista
    # df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: str(x).split(",")[0])
    df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: str(x).split(",")[0])
    df1 = df1.loc[(~df1['cuisines'].isin(['nan','Mineira','Drinks Only'])),:].reset_index(drop=True)
        
    return df1


def country_restaurants(df, titulo = '', eixo_x_titulo = 'country_name', eixo_y_titulo = 'restaurant_id'):
    """
    gera gráfico de barras da quantidades de restaurantes cadastrados por países
    Input: DataFrame, String
    Output: gráfico de barras
    """
    
    df_aux = (df.loc[:,['country_name','restaurant_id']]
             .groupby(['country_name'])
             .nunique()
             .sort_values(['restaurant_id'],ascending=False)
             .reset_index())
    fig = px.bar(df_aux,
                 x='country_name',
                 y='restaurant_id', 
                 title = titulo, 
                 text = 'restaurant_id', 
                 labels = {'country_name': eixo_x_titulo, 'restaurant_id': eixo_y_titulo})

    return fig

def country_city(df, titulo = '', eixo_x_titulo = 'country_name', eixo_y_titulo = 'city'):
    """
    gera gráfico de barras da quantidades de cidades cadastrados por países
    Input: DataFrame, String
    Output: gráfico de barras
    """
    
    df_aux = (df.loc[:,['country_name','city']]
             .groupby(['country_name'])
             .nunique()
             .sort_values(['city'],ascending=False)
             .reset_index())
    fig = px.bar(df_aux,
                 x='country_name',
                 y='city', 
                 title = titulo, 
                 text = 'city', 
                 labels = {'country_name': eixo_x_titulo, 'city': eixo_y_titulo})

    return fig

def country_avg_votes(df, titulo = '', eixo_x_titulo = 'country_name', eixo_y_titulo = 'city'):
    """
    gera gráfico de barras da média de votos nos restaurantes cadastrados por países
    Input: DataFrame, String
    Output: gráfico de barras
    """
    
    df_aux = (df.loc[:,['country_name','restaurant_id','votes']]
                .groupby('country_name')
                .agg({'restaurant_id':['count'],'votes':['mean']}))
    df_aux.columns = ['restaurant_id','votes']
    df_aux = df_aux.sort_values(['votes'],ascending=False).reset_index()
    df_aux['votes'] = df_aux['votes'].apply(lambda x: round(x,2))
    fig = px.bar(df_aux,
                 x='country_name',
                 y='votes', 
                 title = titulo, 
                 text = df_aux['votes'].apply(lambda x: '{:,}'.format(x).replace(',',' ')), 
                 labels = {'country_name': eixo_x_titulo, 'votes': eixo_y_titulo})

    return fig

def country_avg_prices(df, titulo = '', eixo_x_titulo = 'country_name', eixo_y_titulo = 'average_cost_for_two'):
    """
    gera gráfico de barras da média do preço do prato para duas pessoas nos restaurantes cadastrados por países
    Input: DataFrame, String
    Output: gráfico de barras
    """
    
    df_aux = (df.loc[:,['country_name','restaurant_id','average_cost_for_two']]
                .groupby(['country_name'])
                .agg({'average_cost_for_two':['mean']}))
    df_aux.columns = ['average_cost_for_two']
    df_aux = df_aux.sort_values(['average_cost_for_two'],ascending=False).reset_index()
    df_aux['average_cost_for_two'] = df_aux['average_cost_for_two'].apply(lambda x: round(x,2))
    fig = px.bar(df_aux,
                 x='country_name',
                 y='average_cost_for_two', 
                 title = titulo, 
                 text = df_aux['average_cost_for_two'].apply(lambda x: '{:,}'.format(x).replace(',',' ')), 
                 labels = {'country_name': eixo_x_titulo, 'average_cost_for_two': eixo_y_titulo})

    return fig


#___________________Início do código para o Streamlit__________________________________

# Import
df = pd.read_csv('zomato.csv')

#Limpeza
df1 = clean_code(df)

#_______________________________________________________________________________________
#Main Page:


st.set_page_config(
    layout = 'wide',
    page_title='Home',
    page_icon=':bar_chart:'
)


#========================================
#Sidebar no Streamlit
#========================================


with st.sidebar.container():
    col1, col2 = st.columns([1,4])
    with col1:
        image = Image.open('logo.png')
        st.image(image, width=35)
    with col2:
        st.markdown('# Fome Zero')
st.sidebar.markdown('## Filtros')

df_country_names = (df1.loc[df1['country_name'] != 'NaN', 'country_name'].unique())
default_countries = ['Brazil','England','Qatar','South Africa','Canada','Australia']

container = st.sidebar.container()
all = st.sidebar.checkbox("Selecionar todos os países")
if all:
    country_options = st.sidebar.multiselect(
        'Escolha os países que deseja visualizar os restaurantes',
        df_country_names,
        df_country_names,
        )
else:
    country_options = st.sidebar.multiselect(
        'Escolha os países que deseja visualizar os restaurantes',
        df_country_names,
        default = default_countries)

st.sidebar.markdown("""---""")

st.sidebar.markdown('### Powered by André Liziero')

df1_filter = df1.loc[(df1['country_name'].isin(country_options)),:]

#-----------------------------

st.title(':earth_americas: Visão Países')

with st.container():
    fig = country_restaurants(df1_filter, 'Quantidade de Restaurantes Registrados por País', 'Países', 'Quantidade de Restaurantes')
    st.plotly_chart(fig, use_container_width=True, theme = None)

with st.container():
    fig = country_city(df1_filter, 'Quantidade de Cidades Registradas por País', 'Países', 'Quantidade de Cidades')
    st.plotly_chart(fig, use_container_width=True, theme = None)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = country_avg_votes(df1_filter, 'Média de Avaliações feitas por País', 'Países', 'Quantidade de Avaliações')
        st.plotly_chart(fig, use_container_width=True, theme = None)
    with col2:
        fig = country_avg_prices(df1_filter, 'Média de Preço de um prato para duas pessoas por País', 'Países', 'Preço de prato para duas Pessoas')
        st.plotly_chart(fig, use_container_width=True, theme = None)