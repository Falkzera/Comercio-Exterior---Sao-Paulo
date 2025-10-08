import requests
import json
import pandas as pd
import time

url = "https://api-comexstat.mdic.gov.br/cities"

headers = { 
    'Content-Type': "application/json",
    'Accept': "application/json",
}

with open("src/dados/estados.json", 'r', encoding='utf-8') as file:
    estados = json.load(file)["data"]

## Recupera dados da API sobre Importação e Exportação - Sem Filtros
def recuperar_dados(tipoconsulta, datemin, datemax):
    dfs = []

    for estado in estados:
        estado_id = int(estado["id"])
        
        payload = {
            "flow": tipoconsulta,
            "monthDetail": True,
            "period": {
                "from": datemin,
                "to": datemax
            },
            "filters": [
                {"filter": "state", "values": [estado_id]}
            ],
            "details": ["city", "country", "state", "chapter", "economicBlock"],
            "metrics": ["metricFOB"]
        }

        response = requests.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            data = response.json()
            if data.get("data") and data["data"].get("list"):
                df = pd.DataFrame(data["data"]["list"])
                df["flow"] = tipoconsulta
                dfs.append(df)
        else:
            print(f"Request failed with status code {response.status_code}")
        
        time.sleep(10)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()