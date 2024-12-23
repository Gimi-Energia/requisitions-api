from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


def fetch_page(token, secret, page):
    ENDPOINT = "https://api.iniciativaaplicativos.com.br/api/comercial/contratos/lista"
    headers = {"TOKEN": token, "SECRET": secret}
    params = {"offset": 50, "page": page}

    response = requests.get(ENDPOINT, params=params, headers=headers)
    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        print(f"Error on page {page}: {response.status_code}")
        return []


def get_iapp_contracts(token, secret):
    items = []
    max_pages = 400
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_page = {
            executor.submit(fetch_page, token, secret, page): page
            for page in range(1, max_pages + 1)
        }
        for future in as_completed(future_to_page):
            page_items = future.result()
            for item in page_items:
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
