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

    #Criando a coluna 'color_name' com os nomes dos países:
    df1['color_name']=df1['rating_color'].apply(lambda x: color_name(x))
    
    #Removendo linha duplicadas
    df1 = df1.drop_duplicates().reset_index(drop=True)
    
    # Remover restaurantes com culinária 'NaN' e listar apenas o primeiro tipo de culinária da lista
    # df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: str(x).split(",")[0])
    df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: str(x).split(",")[0])
    df1 = df1.loc[(~df1['cuisines'].isin(['nan','Mineira','Drinks Only'])),:].reset_index(drop=True)
        
    return df1

def country_map(df1,fig_title = ''):
    """
    gera mapa da Localização central de cada cidade por tipo de tráfego
    Input: DataFrame, String
    Output: mapa
    """
    st.markdown('##### '+fig_title)
    df_aux = df1.loc[:,['city','latitude','longitude','color_name','restaurant_name','average_cost_for_two','currency','cuisines','aggregate_rating']].reset_index()
    map = folium.Map()
    marker_cluster = MarkerCluster().add_to(map)
    for index, location_info in df_aux.iterrows():
        pop_up = '<b>{}</b><br> <br>Price: {} ({}) para dois.<br>Type:{}<br>Aggregate Rating: {}/5.0'.format(location_info['restaurant_name'],round(location_info['average_cost_for_two'],2),location_info['currency'],location_info['cuisines'],location_info['aggregate_rating'])
        folium.Marker([location_info['latitude'],
                     location_info['longitude']],
                     popup=folium.Popup(pop_up, max_width=300),
                     icon=folium.Icon(color=df_aux.loc[index,'color_name'], icon = 'home',prefix='fa')).add_to(marker_cluster)
    folium_static(map, width=1024, height=778)    

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

#------------------------------

st.markdown('# Fome Zero!')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
#st.markdown('## Temos as seguintes marcas dentro da nossa plataforma:')

with st.container():
    st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        restaurantes = df1['restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados',restaurantes) 
    with col2:
        paises = df1['country_code'].nunique()
        col2.metric('Países Cadastrados',paises) 
    with col3:
        cidades = df1['city'].nunique()
        col3.metric('Cidades Cadastradas',cidades) 
    with col4:
        avaliacoes = '{:,}'.format(df1['votes'].sum()).replace(',','.')
        col4.metric('Avaliações Feitas na Plataforma',avaliacoes) 
    with col5:    
        culinarias = df1['cuisines'].nunique()
        col5.metric('Tipos de Culinárias Oferecidas',culinarias) 

country_map(df1_filter)

