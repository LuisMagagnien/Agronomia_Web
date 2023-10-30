import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso', icon="✅")
    time.sleep(5)
    sucesso.empty()

st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

st.sidebar.title('Filtros')

with st.sidebar.expander('Preço do Produto'):
    preço = st.sidebar.slider('Selecione o preço', 0, 5000, (0, 5000), key="preco_sidebar")

with st.sidebar.expander('Data da compra'):
    data_compra = st.sidebar.date_input('Selecione a data', (dados['Data da Compra'].min().date(), dados['Data da Compra'].max().date()), key="data_compra_sidebar")

with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())

with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0, 5000))

with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0, 250, (0, 250))

with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min().date(), dados['Data da Compra'].max().date()))

with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())

with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect('Selecione o local da compra', dados['Local da compra'].unique(), dados['Local da compra'].unique())

with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra', 1, 5, value=(1, 5))

with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())

with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1, 24))

with st.sidebar.expander('Nome do produto'):
    produtos = st.sidebar.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique(), key="produtos_sidebar")

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

# Converter as datas para datetime
data_compra = (datetime.combine(data_compra[0], datetime.min.time()), datetime.combine(data_compra[1], datetime.max.time()))

# Aplicar os filtros
dados_filtrados = dados[
    (dados['Produto'].isin(produtos)) &
    (dados['Preço'] >= preço[0]) &
    (dados['Preço'] <= preço[1]) &
    (dados['Data da Compra'] >= data_compra[0]) &
    (dados['Data da Compra'] <= data_compra[1])
]

# Exibir os dados filtrados
st.dataframe(dados_filtrados)

# Contador de linhas e colunas
num_linhas, num_colunas = dados_filtrados.shape

# Suponha que num_linhas e num_colunas são variáveis numéricas
formatted_message = f'A tabela possui <span style="color: blue;">{num_linhas}</span> linhas e <span style="color: blue;">{num_colunas}</span> colunas.'

st.markdown(formatted_message, unsafe_allow_html=True)






st.markdown('Escreva um nome para o arquivo')
nome_arquivo = st.text_input('Nome do arquivo', value='dados.csv')

if st.button('Fazer o download da tabela em CSV'):
    st.download_button('Download', converte_csv(dados_filtrados), key='download_button', args=(dados_filtrados, nome_arquivo))

