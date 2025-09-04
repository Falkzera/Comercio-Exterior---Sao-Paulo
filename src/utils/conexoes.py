import pyodbc
from sqlalchemy import create_engine
import urllib.parse

## Usar para cursor.execute, commit, etc.
def abrir_conexao_sql_server():

    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=APIComexstats;"
        "UID=sa;"
        "PWD=@Dev123;"
    )

## Usar para pd.read_sql, suporte para pd
def abrir_engine_sql_server():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=APIComexstats;"
        "UID=sa;"
        "PWD=@Dev123;"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
    params = urllib.parse.quote_plus(conn_str)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)