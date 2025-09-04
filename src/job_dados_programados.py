import argparse
from datetime import date
from src.utils.auxiliar import carregar_ultimo_mes
from src.utils.recuperar_dados_api import recuperar_dados
from src.utils.persistir_dados import salvar_dados_sql_server

## Carrega dados do último mês disponível na API
def main(force: bool = False):
    hoje = date.today()
    if not force and hoje.day < 10:
        return

    ym = carregar_ultimo_mes(hoje)  # ex.: 2025-08 se hoje for 2025-09-10+

    for tipo in ("import", "export"):
        df = recuperar_dados(tipo, ym, ym)
        if df is None or df.empty:
            print(f"[{tipo}] Nada retornado.")
            continue
        print(f"[{tipo}] Linhas: {len(df)} — salvando...")
        salvar_dados_sql_server(df, tipo)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="executa mesmo antes do dia 10")
    args = parser.parse_args()
    main(force=args.force)