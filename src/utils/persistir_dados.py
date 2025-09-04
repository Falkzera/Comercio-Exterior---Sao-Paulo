from src.utils.conexoes import abrir_conexao_sql_server

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
        chapterCode = item['chapterCode']
        chapter = item['chapter']
        economicBlock = item['economicBlock']
        fometricFOBb = item['metricFOB']
        flow = item['flow']

        cursor.execute(f"INSERT INTO {tabela} (noMunMinsguf, year, monthNumber, country, state, chapterCode, chapter, economicBlock, metricFOB, flow) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (noMunMinsguf, year, monthNumber, country, state, chapterCode, chapter, economicBlock, fometricFOBb, flow))

    conn.commit()
    conn.close()