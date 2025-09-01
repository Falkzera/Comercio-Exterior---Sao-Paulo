import requests
import json
import pandas as pd

url = "https://api-comexstat.mdic.gov.br/cities"

def recuperar_dados(tipoconsulta, datemin, datemax):

    ## Tipos de consulta
    # export - Exortação
    # import - Importação

    payload = {
        "flow": tipoconsulta,
        "monthDetail": False,
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