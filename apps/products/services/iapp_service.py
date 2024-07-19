from uuid import uuid4

import requests
import os

def get_iapp_products(offset=50000):
    """
    Obtém os produtos da API Iniciativa Aplicativos.

    Args:
        offset (int, optional): O valor de deslocamento para a consulta paginada. O padrão é 50000.

    Returns:
        list: Uma lista de dicionários contendo informações dos produtos.
            Cada dicionário possui as seguintes chaves:
                - code (str): O código do produto.
                - un (str): A unidade de medida do produto.
                - description (str): A descrição do produto.

            Retorna None em caso de erro na requisição.
    """
    token = str(os.getenv("TOKEN_GBL"))
    secret = str(os.getenv("SECRET_GBL"))
    
    ENDPOINT = "https://api.iniciativaaplicativos.com.br/api/engenharia/produtos/lista"
    headers = {"TOKEN": token, "SECRET": secret}

    params = {"offset": offset, "page": 1, "filters": "status|0"}

    response = requests.get(ENDPOINT, params=params, headers=headers)
    print('RESPONSE: ', response.ok)
    
    if response.ok:
        iapp_response = response.json()
        if iapp_response['success'] is False:
            raise Exception(iapp_response['message'])
        items = [
            {
                "code": item["identificacao"],
                "un": item["unidade_medida"],
                "description": item["descricao"],
            }
            for item in iapp_response["response"]
        ]
        return items
    else:
        print("Error:", response.status_code)
        return None
