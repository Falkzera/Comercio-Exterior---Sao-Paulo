import streamlit as st
import pandas as pd
from src.utils.recuperar_dados_bd import carregar_dados
from src.utils.auxiliar import carregar_dados_ano_por_ano
from src.job_dados_programados import main

st.set_page_config(layout="wide")

opt_consulta = st.sidebar.selectbox('Tipo de Dados', ['Importação', 'Exportação'])

st.sidebar.date_input('Período', [])

colunas_visiveis = {
    'Importação': ['noMunMinsgUf', 'year', 'monthNumber', 'country', 'state', 'chapter', 'economicBlock', 'metricFOB'],
    'Exportação': ['noMunMinsgUf', 'year', 'monthNumber', 'country', 'state', 'chapter', 'economicBlock', 'metricFOB'],
}

colunas_config = {
    "noMunMinsgUf": st.column_config.TextColumn("Município"),
    "year": st.column_config.TextColumn("Ano"),
    "monthNumber": st.column_config.TextColumn("Mês"),
    "country": st.column_config.TextColumn("País"),
    "state": st.column_config.TextColumn("Estado"),
    "chapter": st.column_config.TextColumn("Materias"),
    "economicBlock": st.column_config.TextColumn("Bloco Econômico"),
    "metricFOB": st.column_config.NumberColumn("Valor FOB (Dólar)", format="%.2f"),
}

@st.cache_data
def carregar_dados_pagina(opt_consulta):  
    if opt_consulta == 'Importação':
        df = carregar_dados('Importacao')
        st.dataframe(df[colunas_visiveis['Importação']], width='stretch', height=750, hide_index=True, column_config=colunas_config)
    elif opt_consulta == 'Exportação':
        df = carregar_dados('Exportacao')
        st.dataframe(df[colunas_visiveis['Exportação']], width='stretch', height=750, hide_index=True, column_config=colunas_config)
    return df

if st.sidebar.button('Carregar Dados', type='primary'):
    df = carregar_dados_pagina(opt_consulta)
    if not df.empty:
        st.sidebar.success('Dados carregados com sucesso!')
    else:
        st.sidebar.error('Erro ao buscar os dados')