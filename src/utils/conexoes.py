import pyodbc

def abrir_conexao_sql_server():

    server = 'localhost,1433'
    database = 'APIComexstats'
    username = 'sa'
    password = '@Dev123'

    conn = pyodbc.connect(f'DRIVER={{SQL Server}};'
                        f'SERVER={server};'
                        f'DATABASE={database};'
                        f'UID={username};'
                        f'PWD={password}')

    return conn