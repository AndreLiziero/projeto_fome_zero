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


def city_restaurants(df, titulo = '', eixo_x_titulo = 'city', eixo_y_titulo = 'restaurant_id', legenda = 'country_name'):
    """
    gera gráfico de barras das top 10 cidades com mais restaurantes cadastrados
    Input: DataFrame, String
    Output: gráfico de barras
    """
    
    df_aux = (df.loc[:,['city','restaurant_id','country_name']]
                .groupby(['city','country_name'])
                .nunique()
                .sort_values(['restaurant_id'],ascending=False)
                .reset_index())
    df_aux = df_aux.iloc[0:10,:]
    fig = px.bar(df_aux,
                 x = 'city',
                 y = 'restaurant_id', 
                 color = 'country_name', 
                 title = titulo, 
                 text = 'restaurant_id', 
                 labels = {'city': eixo_x_titulo, 'restaurant_id': eixo_y_titulo, 'country_name': legenda})

    return fig

def city_top7(df, titulo = '', eixo_x_titulo = 'city', eixo_y_titulo = 'restaurant_id', legenda = 'country_name'):
    """
    gera gráfico de barras das top 7 cidades com restaurantes com média de avaliação acima de 4
    Input: DataFrame, String
    Output: gráfico de barras
    """
    
    df_aux = (df.loc[df['aggregate_rating'] > 4,['city','country_name','restaurant_id']]
                 .groupby(['city','country_name'])
                 .nunique()
                 .sort_values(['restaurant_id'],ascending=False)
                 .reset_index())
    df_aux = df_aux.iloc[0:7,:]
    fig = px.bar(df_aux,
                 x='city',
                 y='restaurant_id', 
                 color = 'country_name', 
                 title = titulo, 
                 text = 'restaurant_id', 
                 labels = {'city': eixo_x_titulo, 'restaurant_id': eixo_y_titulo, 'country_name': legenda})

    return fig

def city_bot7(df, titulo = '', eixo_x_titulo = 'city', eixo_y_titulo = 'restaurant_id', legenda = 'country_name'):
    """
    gera gráfico de barras das top 7 cidades com restaurantes com média de avaliação abaixo de 2.5
    Input: DataFrame, String
    Output: gráfico de barras
    """
    
    df_aux = (df.loc[df['aggregate_rating'] < 2.5,['city','country_name','restaurant_id']]
                 .groupby(['city','country_name'])
                 .nunique()
                 .sort_values(['restaurant_id'],ascending=False)
                 .reset_index())
    df_aux = df_aux.iloc[0:7,:]
    fig = px.bar(df_aux,
                 x='city',
                 y='restaurant_id', 
                 color = 'country_name', 
                 title = titulo, 
                 text = 'restaurant_id', 
                 labels = {'city': eixo_x_titulo, 'restaurant_id': eixo_y_titulo, 'country_name': legenda})

    return fig

def city_cuisines(df, titulo = '', eixo_x_titulo = 'city', eixo_y_titulo = 'cuisines', legenda = 'country_name'):
    """
    gera gráfico de barras do top 10 cidades com maior varidade de tipos culinários
    Input: DataFrame, String
    Output: gráfico de barras
    """
    
    df_aux = (df.loc[:,['city','cuisines','country_name']]
                 .groupby(['city','country_name'])
                 .nunique()
                 .sort_values(['cuisines'],ascending=False)
                 .reset_index())
    df_aux = df_aux.iloc[0:10,:]
    fig = px.bar(df_aux,
                 x = 'city',
                 y = 'cuisines',
                 color = 'country_name',
                 title = titulo, 
                 text = 'cuisines', 
                 labels = {'city': eixo_x_titulo, 'cuisines': eixo_y_titulo, 'country_name': legenda})

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

st.title(':cityscape: Visão Cidades')

with st.container():
    fig = city_restaurants(df1_filter, 'Top 10 Cidades com mais Restaurantes na Base de Dados', 'Cidade', 'Quantidade de Restaurantes', 'País')
    st.plotly_chart(fig, use_container_width=True, theme = None)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = city_top7(df1_filter, 'Top 7 Cidades com Restaurantes com média de avaliação acima de 4', 'Cidade', 'Quantidade de Restaurantes', 'Países')
        st.plotly_chart(fig, use_container_width=True, theme = None)
    with col2:
        fig = city_bot7(df1_filter, 'Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5', 'Cidade', 'Quantidade de Reataurantes', 'Países')
        st.plotly_chart(fig, use_container_width=True, theme = None)

with st.container():
    fig = city_cuisines(df1_filter, 'Top 10 Cidades mais restaurantes com tipos culinários distintos', 'Cidade', 'Quantidade de Tipos Culinários Únicos', 'Países')
    st.plotly_chart(fig, use_container_width=True, theme = None)