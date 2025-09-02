import requests
import json
import pandas as pd
import time
from src.utils.conexoes import abrir_conexao_sql_server

url = "https://api-comexstat.mdic.gov.br/cities"

def carregar_dados_sql_server(tipo):
    
    conn = abrir_conexao_sql_server()
    query = f"SELECT * FROM Dados{tipo}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def recuperar_dados(tipoconsulta, datemin, datemax):

    ## Tipos de consulta
    # export - Exortação
    # import - Importação

    payload = {
        "flow": tipoconsulta,
        "monthDetail": True,
        "period": {
            "from": datemin,
            "to": datemax
        },
        "filters": [
            {"filter": "state", "values": [41]}
        ],
        "details": ["city", "country", "state"],
        "metrics": ["metricFOB"]
    }

    headers = { 
        'Content-Type': "application/json",
        'Accept': "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        if data.get("data") and data["data"].get("list"):
            df = pd.DataFrame(data["data"]["list"])
            df["flow"] = tipoconsulta
        return df
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

## Salva os dados na tabela correspondente
def salvar_dados_sql_server(dados, tipo):
    conn = abrir_conexao_sql_server()
    cursor = conn.cursor()

    if tipo == 'import':
        tabela = 'DadosImportacao'        
    elif tipo == 'export':
        tabela = 'DadosExportacao'

    for _, item in dados.iterrows():
        noMunMinsguf = item['noMunMinsgUf']
        year = item['year']
        monthNumber = item['monthNumber']
        country = item['country']
        state = item['state']
        fometricFOBb = item['metricFOB']
        flow = item['flow']

        cursor.execute(f"INSERT INTO {tabela} (noMunMinsguf, year, monthNumber, country, state, metricFOB, flow) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (noMunMinsguf, year, monthNumber, country, state, fometricFOBb, flow))

    conn.commit()
    conn.close()

## Carrega dados por ano desde 1997
def carregar_dados_ano_por_ano():
    for ano in range(1997, 2025):  # De 1997 até 2024
        datemin = f"{ano}-01"
        datemax = f"{ano}-12"

        print(f"Recuperando dados de {datemin} a {datemax}")
            
        dados_import = recuperar_dados("import", datemin, datemax)
        if dados_import is not None and isinstance(dados_import, pd.DataFrame) and not dados_import.empty:
            salvar_dados_sql_server(dados_import, 'import')

        dados_export = recuperar_dados("export", datemin, datemax)
        if dados_export is not None and isinstance(dados_export, pd.DataFrame) and not dados_export.empty:
            salvar_dados_sql_server(dados_export, 'export')

        time.sleep(60)

    # Combina todos os dataframes em um único dataframe
    df_final = pd.concat(todos_dados, ignore_index=True)
    return df_final

# Chamar a função para carregar todos os dados
## dados = carregar_dados_ano_por_ano()