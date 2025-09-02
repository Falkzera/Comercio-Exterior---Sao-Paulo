import streamlit as st
import pandas as pd
from src.recuperar_dados import carregar_dados_sql_server

opt_consulta = st.sidebar.selectbox('Tipo de Dados', ['Importação', 'Exportação'])

st.sidebar.date_input('Período', [])

@st.cache_data
def carregar_dados_pagina(opt_consulta):  
    if opt_consulta == 'Importação':
        df = carregar_dados_sql_server('Importacao')
        st.dataframe(df)
    elif opt_consulta == 'Exportação':
        df = carregar_dados_sql_server('Exportacao')
        st.dataframe(df)
    return df

if st.sidebar.button('Carregar Dados', type='primary'):
    carregar_dados_pagina(opt_consulta)