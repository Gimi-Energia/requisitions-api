from uuid import uuid4

import requests


def get_iapp_products(token, secret):
    ENDPOINT = "https://iapp.iniciativaaplicativos.com.br/api/engenharia/produtos/lista"
    offset = 50000

    headers = {"TOKEN": token, "SECRET": secret}

    params = {"offset": offset, "page": 1}

    response = requests.get(ENDPOINT, params=params, headers=headers)

    if response.status_code == 200:
        complete_data = response.json()
        data = complete_data["response"]
        items = []
        for item in data:
            if item["status"] == "ativo":
                item_info = {
                    "id": str(uuid4()),
                    "code": item["identificacao"],
                    "un": item["unidade_medida"],
                    "description": item["descricao"],
                }
                items.append(item_info)
        return items
    else:
        print("Error:", response.status_code)
        return None
