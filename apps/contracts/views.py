import os

import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.contracts.models import Contract
from apps.contracts.serializers import ContractSerializer
from utils.permissions import IsAdminPost, IsAuthenticatedGet


class ContractsDataAPIView(APIView):
    def fetch_data_list(self, page, token, secret):
        ENDPOINT = "https://ia1.iapp03.iniciativaaplicativos.com.br/api/comercial/contratos/lista"
        offset = 50

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
                        "company": {3060: "Gimi", 3061: "GBL", 3062: "GPB", 3464: "GIR"}.get(
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

    def get(self, request):
        company = str(request.headers.get("Company", None)).upper()

        token = str(os.getenv(f"TOKEN_{company}"))
        secret = str(os.getenv(f"SECRET_{company}"))

        if not company:
            return Response(
                {"message": "Token and secret are required in headers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        MAX_PAGES = 1000

        try:
            for page_number in range(1, MAX_PAGES + 1):
                items = self.fetch_data_list(page_number, token, secret)

                if not items:
                    break

                for item in items:
                    Contract.objects.update_or_create(
                        id=item["id"],
                        defaults={
                            "company": item["company"],
                            "contract_number": item["contract_number"],
                            "control_number": item["control_number"],
                            "client_name": item["client_name"],
                            "project_name": item["project_name"],
                            "freight_estimated": item["freight_estimated"],
                        },
                    )

                    print(item["contract_number"])

            return Response({"message": "Data entered successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "Error inserting data: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ContractList(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["contract_number", "company"]
    ordering_fields = []
    filterset_fields = ["company", "contract_number"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedGet()]
        elif self.request.method == "POST":
            return [IsAdminPost()]
        return super().get_permissions()


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
