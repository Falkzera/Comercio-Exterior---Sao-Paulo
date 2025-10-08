from src.utils.conexoes import abrir_engine_sql_server
import pandas as pd
from sqlalchemy import text

## Carrega dados do banco de dados - Importação e Exportação
def carregar_dados(tipo, mes_ini, mes_fim, ano_ini, ano_fim):
    engine = abrir_engine_sql_server()
    with engine.connect() as conn: ## usar .begin para casos de transação, .connect para apenas consultas simples
        return pd.read_sql(text(f"SELECT * FROM Dados{tipo} WHERE monthNumber BETWEEN {mes_ini} AND {mes_fim} AND year BETWEEN {ano_ini} AND {ano_fim}"), conn) 

# Carrega todos os usuários
def carregar_usuarios():
    engine = abrir_engine_sql_server()
    with engine.connect() as conn: ## usar .begin para casos de transação, .connect para apenas consultas simples
        return pd.read_sql(text(f"SELECT * FROM Usuarios"), conn) 

# Carrega um usuário pelo ID
def carregar_usuario_id(user_id: int):
    engine = abrir_engine_sql_server()
    with engine.connect() as conn:
        return conn.execute(text("SELECT * FROM Usuarios WHERE idUsuario=:idUsuario"), {"idUsuario": user_id}).fetchone()
    
# Verifica se o e-mail já existe no banco de dados
def email_existe(email: str) -> bool:
    engine = abrir_engine_sql_server()
    with engine.connect() as conn:
        r = conn.execute(text("SELECT 1 FROM Usuarios WHERE LOWER(email)=LOWER(:e)"), {"e": email.strip()}).fetchone()
        return r is not None
