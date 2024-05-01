import requests

def get_iapp_contracts(page, token, secret):
    ENDPOINT = "https://api.iniciativaaplicativos.com.br/api/comercial/contratos/lista"
    offset = 30

    headers = {"TOKEN": token, "SECRET": secret}

    params = {"offset": offset, "page": page}

    response = requests.get(ENDPOINT, params=params, headers=headers)

    if response.status_code == 200:
        complete_data = response.json()
        data = complete_data["response"]
        items = []
        for item in data:
            if item["status"] != "CANCELADO" and item["etapa"] != "CANCELADO":
                item_info = {
                    "id": str(item["id"]),
                    "company": {687: "Gimi", 688: "GBL", 689: "GPB", 690: "GIR"}.get(
                        item["codigo_empresa"], None
                    ),
                    "contract_number": item["identificacao"],
                    "control_number": item["numero_controle"],
                    "client_name": item["cliente"]["nome"],
                    "project_name": item["projeto"]["nome"],
                    "freight_estimated": item["valores"]["valor_frete"],
                }
                items.append(item_info)
        return items
    else:
        print("Error:", response.status_code)
        return None
