import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
from src.utils.recuperar_dados_bd import carregar_dados
from src.utils.autenticacao import exigir_login

exigir_login(["admin", "analista", "viewer"]) # Permissões de visualização, todos

st.set_page_config(layout="wide")
st.sidebar.markdown("<h3 style='margin-bottom:0'>📊 Visualizacão Geral</h3>", unsafe_allow_html=True)
st.title("Dados filtrados")
st.markdown("### Dados brutos de Importação e Exportação do Brasil")

opt_consulta = st.sidebar.selectbox('**Tipo de Dados**', ['Importação', 'Exportação'])

hoje = datetime.now()
anos = list(range(1997, hoje.year + 1))
meses = list(range(1, 13))

# Seletor personalizado
st.sidebar.markdown("**Período**")
c1, c2 = st.sidebar.columns(2)
mes_ini_sel = c1.selectbox("Mês inicial", meses, format_func=lambda m: f"{m:02d}", index=hoje.month-2)
ano_ini_sel = c2.selectbox("Ano inicial", anos, index=len(anos)-1)

c3, c4 = st.sidebar.columns(2)
mes_fim_sel = c3.selectbox("Mês final", meses, format_func=lambda m: f"{m:02d}", index=hoje.month-2)
ano_fim_sel = c4.selectbox("Ano final", anos, index=len(anos)-1)

st.sidebar.markdown("---")

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

@st.cache_data(ttl=600, show_spinner="Consultando dados...")
def carregar_dados_pagina(opt_consulta, mes_ini_sel, mes_fim_sel, ano_ini_sel, ano_fim_sel):
    # Mapeia rótulo -> sufixo da tabela
    tipo_sql = 'Importacao' if opt_consulta == 'Importação' else 'Exportacao'
    df = carregar_dados(tipo_sql, mes_ini_sel, mes_fim_sel, ano_ini_sel, ano_fim_sel)

    # Renderiza a tabela correspondente ao tipo escolhido
    st.dataframe(
        df[colunas_visiveis[opt_consulta]],
        # width='stretch',	
        height=750,
        hide_index=True,
        column_config=colunas_config
    )
    return df

if st.sidebar.button('Carregar Dados', type='primary'):
    ini_key = int(ano_ini_sel) * 100 + int(mes_ini_sel)
    fim_key = int(ano_fim_sel) * 100 + int(mes_fim_sel)
    if ini_key > fim_key:
        st.sidebar.error('Período inválido: Data Inicial maior que Data Final')
        st.stop()

    df = carregar_dados_pagina(opt_consulta, mes_ini_sel, mes_fim_sel, ano_ini_sel, ano_fim_sel)
    if not df.empty:
        st.sidebar.success('Dados carregados com sucesso!')
    else:
        st.sidebar.error('Sem dados no período selecionado')
else:
    # Mensagem inicial
    st.info("👈 Selecione os filtros desejados e clique em 'Carregar Dados' para visualizar os dados brutos")