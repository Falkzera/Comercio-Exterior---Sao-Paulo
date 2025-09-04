import streamlit as st
import pandas as pd
from src.utils.auxiliar import carregar_dados_ano_por_ano
from src.job_dados_programados import main

## Atenção: botão provisório para carregar todos os dados, por enquanto não há uma lógica para ver se os registros já existem.
if st.sidebar.button('Carregar Todos os Dados', type='primary'):
    carregar_dados_ano_por_ano()

if st.sidebar.button('Carregar Dados Mês Anterior', type='primary'):
    main(force = True)