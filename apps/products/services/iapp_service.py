from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


def fetch_page(token, secret, page):
    ENDPOINT = "https://api.iniciativaaplicativos.com.br/api/engenharia/produtos/lista"
    headers = {"TOKEN": token, "SECRET": secret}
    params = {"offset": 1000, "page": page, "filters": "status|0"}

    response = requests.get(ENDPOINT, params=params, headers=headers)
    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        print(f"Error on page {page}: {response.status_code}")
        return []


def get_iapp_products(token, secret):
    items = []
    max_pages = 30
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_page = {
            executor.submit(fetch_page, token, secret, page): page
            for page in range(1, max_pages + 1)
        }
        for future in as_completed(future_to_page):
            page_items = future.result()
            for item in page_items:
                item_info = {
                    "code": item["identificacao"],
                    "un": item["unidade_medida"],
                    "description": item["descricao"],
                }
                items.append(item_info)
    return items
