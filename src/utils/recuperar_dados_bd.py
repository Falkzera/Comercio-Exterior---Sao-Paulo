from src.utils.conexoes import abrir_conexao_sql_server, abrir_engine_sql_server
import pandas as pd
from sqlalchemy import text

## Carrega dados do banco de dados - Importação e Exportação
def carregar_dados(tipo):
    engine = abrir_engine_sql_server()
    with engine.connect() as conn: ## usar .begin para casos de transação, .connect para apenas consultas simples
        return pd.read_sql(text(f"SELECT * FROM Dados{tipo}"), conn) 