import json
import os

import requests

from apps.purchases.models import PurchaseProduct


def include_purchase_requisition(instance):
    try:
        omie_app_key = str(
            os.getenv(f"OMIE_APP_KEY_{instance.company}", str(os.getenv("OMIE_APP_KEY_GIMI")))
        )
        omie_app_secret = str(
            os.getenv(f"OMIE_APP_SECRET_{instance.company}", str(os.getenv("OMIE_APP_SECRET_GIMI")))
        )
        url = "https://app.omie.com.br/api/v1/produtos/requisicaocompra/"
        purchase_products = PurchaseProduct.objects.filter(purchase=instance.id, status="Approved")
        item_number = 1
        data = []
        for purchase_product in purchase_products:
            if "GENERIC" in purchase_product.product.code:
                return
            product_code = get_omie_product_code(purchase_product.product.code, instance.company)
            row = {
                "codItem": str(item_number),
                "codProd": product_code,
                "precoUnit": float(purchase_product.price),
                "qtde": float(purchase_product.quantity),
            }
            data.append(row)
            item_number += 1
        categories = {"Gimi": "2.01.73", "GBL": "2.10.93", "GPB": "2.04.95", "GS": "2.10.97"}
        payload = json.dumps(
            {
                "call": "IncluirReq",
                "param": [
                    {
                        "codCateg": categories.get(instance.company, "2.01.73"),
                        "codIntReqCompra": f"INT-{instance.control_number}",
                        "dtSugestao": instance.request_date.strftime("%d/%m/%Y"),
                        "obsReqCompra": instance.obs,
                        "obsIntReqCompra": f"""
                        NC Interno: {instance.control_number} 
                        Requisitante: {instance.requester}
                        Departamento: {instance.department.name}
                        """,
                        "ItensReqCompra": data,
                    }
                ],
                "app_key": omie_app_key,
                "app_secret": omie_app_secret,
            }
        )
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=payload)
        return response
    except Exception:
        return False


def get_omie_product_code(code, company):
    omie_app_key = str(os.getenv(f"OMIE_APP_KEY_{company}", str(os.getenv("OMIE_APP_KEY_GIMI"))))
    omie_app_secret = str(
        os.getenv(f"OMIE_APP_SECRET_{company}", str(os.getenv("OMIE_APP_SECRET_GIMI")))
    )
    url = "https://app.omie.com.br/api/v1/geral/produtos/"

    payload = json.dumps(
        {
            "call": "ConsultarProduto",
            "param": [{"codigo": code}],
            "app_key": omie_app_key,
            "app_secret": omie_app_secret,
        }
    )

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        return f"Erro {response.status_code} ao enviar requisição para Omie: {response.text}"

    response_data = response.json()

    return response_data["codigo_produto"]
