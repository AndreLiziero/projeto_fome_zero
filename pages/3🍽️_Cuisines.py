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

def top_dataframe(df, titulo = '', quantidade = 10):
    st.markdown('## '+titulo)
    df_aux = (df.loc[:,['restaurant_id',
                        'restaurant_name',
                        'country_name',
                        'city',
                        'cuisines',
                        'average_cost_for_two',
                        'aggregate_rating',
                        'votes']]
                .sort_values(['aggregate_rating','restaurant_id'], ascending=[False,True])
                .reset_index(drop=True)
                .head(quantidade)
             )
    return df_aux

def metric_ratings(df, legenda = '', cozinha = ''):
    help_text = 'País: {} \n \nCidade: {} \n \nMédia de Prato para dois: {} ({})'
    coz = df.loc[df['cuisines'] == cozinha, ['country_name','city','restaurant_id','restaurant_name','cuisines','average_cost_for_two','currency','aggregate_rating',]].sort_values(['aggregate_rating','restaurant_id'], ascending=[False,True]).iloc[0,:]
    return st.metric(label = legenda+': '+coz['restaurant_name'],value = str(coz['aggregate_rating'])+'/5.0', help = help_text.format(coz['country_name'],coz['city'],coz['average_cost_for_two'],coz['currency']))


def top_cuisines(df,  titulo = '', eixo_x_titulo = 'cuisines', eixo_y_titulo = 'aggregate_rating', list = 'top', quantidade = 10):
    if list == 'top':
        asc = False
    elif list == 'bottom':
        asc = True

    df_aux = df.loc[:,['cuisines','aggregate_rating']].groupby('cuisines').agg({'aggregate_rating': 'mean'})
    df_aux.columns = ['avg_agg_rating']
    df_aux['avg_agg_rating'] = df_aux.loc[df_aux['avg_agg_rating']>0,'avg_agg_rating'].apply(lambda x: round(x,2))
    df_aux = df_aux.sort_values('avg_agg_rating',ascending = asc).reset_index().iloc[0:quantidade,:]
    fig = px.bar(df_aux,
                x='cuisines',
                y='avg_agg_rating', 
                title = titulo, 
                text = 'avg_agg_rating', 
                labels = {'cuisines': eixo_x_titulo, 'avg_agg_rating': eixo_y_titulo})

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
all_countries = st.sidebar.checkbox("Selecionar todos os países")
if all_countries:
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


restaurant_slider = st.sidebar.slider(
    'Selecione a quantidade de Restaurantes que deseja visualizar',
    min_value = 1,
    max_value = 20,
    value = 10
)


df_cuisines = (df1.loc[df1['cuisines'] != 'NaN', 'cuisines'].unique())
default_cuisines = ['Home-made','BBQ','Japanese','Arabian','American', 'Italian', 'Brazilian']

container = st.sidebar.container()
all_cuisines = st.sidebar.checkbox("Selecionar todos os tipos de culinárias")
if all_cuisines:
    cuisines_options = st.sidebar.multiselect(
        'Escolha os Tipos de Culinária',
        df_cuisines,
        df_cuisines)
else:
    cuisines_options = st.sidebar.multiselect(
        'Escolha os Tipos de Culinária',
        df_cuisines,
        default = default_cuisines)




st.sidebar.markdown("""---""")

st.sidebar.markdown('### Powered by André Liziero')

df1_filter = df1.loc[(df1['country_name'].isin(country_options) & df1['cuisines'].isin(cuisines_options)),:]
df2_filter = df1.loc[df1['country_name'].isin(country_options),:]

#-----------------------------

st.title(':knife_fork_plate: Visão Tipos de Culinárias/Cozinhas')
st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        metric_ratings(df1, legenda = 'Italiana', cozinha = 'Italian')
    with col2:
        metric_ratings(df1, legenda = 'Brasileira', cozinha = 'Brazilian')
    with col3:
        metric_ratings(df1, legenda = 'Japonesa', cozinha = 'Japanese')
    with col4:
        metric_ratings(df1, legenda = 'Americana', cozinha = 'American')
    with col5:    
        metric_ratings(df1, legenda = 'BBQ', cozinha = 'BBQ')
with st.container():
    st.dataframe(top_dataframe(df1_filter,'Top '+str(restaurant_slider)+' Restaurantes',quantidade = restaurant_slider),use_container_width=True)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = top_cuisines(df2_filter, titulo = 'Top {} Melhores Tipos de Culinárias'.format(str(restaurant_slider)), eixo_x_titulo = 'Tipo de Culinária', eixo_y_titulo = 'Avaliação Média', list = 'top', quantidade = restaurant_slider)
        st.plotly_chart(fig, use_container_width=True, theme = None)
    with col2:
        fig = top_cuisines(df2_filter, titulo = 'Top {} Piores Tipos de Culinárias'.format(str(restaurant_slider)), eixo_x_titulo = 'Tipo de Culinária', eixo_y_titulo = 'Avaliação Média', list = 'bottom', quantidade = restaurant_slider)
        st.plotly_chart(fig, use_container_width=True, theme = None)







