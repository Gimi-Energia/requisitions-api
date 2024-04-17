import os

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.contracts.models import Contract
from apps.contracts.serializers import ContractSerializer
from utils.permissions import IsAdminPost, IsAuthenticatedGet

from .services.iapp_service import get_iapp_contracts


class ContractsDataAPIView(APIView):
    def get(self, request):
        company = str(request.headers.get("Company", None)).upper()

        if not company:
            return Response(
                {"message": "Company are required in headers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = str(os.getenv(f"TOKEN_{company}"))
        secret = str(os.getenv(f"SECRET_{company}"))

        init = {"GIMI": 233, "GBL": 79, "GPB": 91, "GIR": 3}

        MAX_PAGES = 1000

        try:
            for page_number in range(init[company], MAX_PAGES + 1):
                items = get_iapp_contracts(page_number, token, secret)

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
    ordering_fields = ["contract_number", "freight_consumed"]
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
