import json
import os
import time
from uuid import uuid4

import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from utils.permissions import IsAdminPost, IsAuthenticatedGet


class ProductsDataAPIView(APIView):
    def fetch_data_list(self, page, token, secret):
        ENDPOINT = "https://ia1.iapp03.iniciativaaplicativos.com.br/api/engenharia/produtos/lista"
        offset = 150

        headers = {"TOKEN": token, "SECRET": secret}

        params = {"offset": offset, "page": page}

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

    def get(self, request):
        token = str(os.getenv("TOKEN_GIMI"))
        secret = str(os.getenv("SECRET_GIMI"))

        MAX_PAGES = 1000

        try:
            for page_number in range(1, MAX_PAGES + 1):
                items = self.fetch_data_list(page_number, token, secret)

                if not items:
                    break

                for item in items:
                    product_id = item["id"]
                    existing_product = Product.objects.filter(id=product_id).first()

                    if not existing_product:
                        new_product = Product(
                            id=item["id"],
                            code=item["code"],
                            un=item["un"],
                            description=item["description"],
                        )
                        new_product.save()

                time.sleep(1)

            return Response({"message": "Data entered successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "Error inserting data: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["code", "un"]
    ordering_fields = ["code", "un", "price"]
    filterset_fields = ["code"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedGet()]
        elif self.request.method == "POST":
            return [IsAdminPost()]
        return super().get_permissions()


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
