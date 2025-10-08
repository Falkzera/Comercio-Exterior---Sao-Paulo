import bcrypt
from src.utils.conexoes import abrir_conexao_sql_server

def gerar_hash_senha(senha_plana: str) -> str:
    sal = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(senha_plana.encode("utf-8"), sal).decode("utf-8")

## Salva os dados na tabela correspondente
def salvar_dados_sql_server(dados, tipo):
    conn = abrir_conexao_sql_server()
    cursor = conn.cursor()

    if tipo == 'import':
        tabela = 'DadosImportacao'        
    elif tipo == 'export':
        tabela = 'DadosExportacao'

    for _, item in dados.iterrows():
        noMunMinsguf  = item['noMunMinsgUf']
        year          = item['year']
        monthNumber   = item['monthNumber']
        country       = item['country']
        state         = item['state']
        chapterCode   = item['chapterCode']
        chapter       = item['chapter']
        economicBlock = item['economicBlock']
        fometricFOBb  = item['metricFOB']
        flow = item['flow']

        cursor.execute(f"INSERT INTO {tabela} (noMunMinsguf, year, monthNumber, country, state, chapterCode, chapter, economicBlock, metricFOB, flow) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (noMunMinsguf, year, monthNumber, country, state, chapterCode, chapter, economicBlock, fometricFOBb, flow))

    conn.commit()
    conn.close()

# Insere novo usuário na tabela
def cadastrar_usuario(nome: str, email: str, perfil: str, ativo: bool, senha: str):
    conn = abrir_conexao_sql_server()
    cursor = conn.cursor()
    try:
        senha_hash = gerar_hash_senha(senha)
        cursor.execute("INSERT INTO Usuarios (nome, email, perfil, ativo, senha_hash) VALUES (?, ?, ?, ?, ?)", (nome.strip(), email.strip(), perfil, 1 if ativo else 0, senha_hash))
        conn.commit()
        return True
    except Exception as e:
        raise
    finally:
        conn.close()

# Atualizar dados de um usuário
def atualizar_usuario(user_id: int, *, nome: str = None, email: str = None, perfil: str = None, ativo: bool = None, senha_hash: str = None, ultimo_login: str = None) -> bool:
    sets = []
    valores = []
    if nome is not None:
        sets.append("nome = ?"); valores.append(nome.strip())
    if email is not None:
        sets.append("email = ?"); valores.append(email.strip().lower())
    if perfil is not None:
        sets.append("perfil = ?"); valores.append(perfil)
    if ativo is not None:
        sets.append("ativo = ?"); valores.append(1 if ativo else 0)
    if senha_hash is not None:
        sets.append("senha_hash = ?"); valores.append(senha_hash)
    if ultimo_login is not None:
        sets.append("ultimo_login = ?"); valores.append(ultimo_login)
    
    if not sets:
        return False

    sql = f"UPDATE Usuarios SET {', '.join(sets)} WHERE idUsuario = ?"
    valores.append(user_id)
    conn = abrir_conexao_sql_server()
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql, valores)
        conn.commit()
        return True
    except Exception as e:
        raise
    finally:
        cursor.close()
        conn.close()