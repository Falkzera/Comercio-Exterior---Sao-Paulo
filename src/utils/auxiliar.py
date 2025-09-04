import pandas as pd
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from src.utils.recuperar_dados_api import recuperar_dados
from src.utils.persistir_dados import salvar_dados_sql_server

## Carrega o último mês de acordo com a data
def carregar_ultimo_mes(data=None):
    if data is None:
        data = date.today()
    primeiro_dia_deste_mes = data.replace(day=1)
    ultima_dia_mes_passado = primeiro_dia_deste_mes - relativedelta(days=1)
    return f"{ultima_dia_mes_passado.year}-{ultima_dia_mes_passado.month:02d}"

## Carrega dados por ano desde 1997 de cada ano e mês e salva no banco de dados
def carregar_dados_ano_por_ano():
    for ano in range(1997, 2025):  # De 1997 até 2024
        for mes in range(1, 13):
            datemin = f"{ano}-{mes:02d}"
            datemax = f"{ano}-{mes:02d}"

            print(f"Recuperando dados de {datemin} a {datemax}")
                
            dados_import = recuperar_dados("import", datemin, datemax)
            if dados_import is not None and isinstance(dados_import, pd.DataFrame) and not dados_import.empty:
                salvar_dados_sql_server(dados_import, 'import')

            dados_export = recuperar_dados("export", datemin, datemax)
            if dados_export is not None and isinstance(dados_export, pd.DataFrame) and not dados_export.empty:
                salvar_dados_sql_server(dados_export, 'export')

            time.sleep(20)
    return None