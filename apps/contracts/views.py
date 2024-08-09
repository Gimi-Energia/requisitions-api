import os

from django.db import transaction
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

        try:
            items = get_iapp_contracts(token, secret)

            if not items:
                return Response(
                    {"message": "Error finding contracts"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            contracts_to_create = []
            existing_contract_ids = set(
                Contract.objects.filter(id__in=[item["id"] for item in items]).values_list(
                    "id", flat=True
                )
            )
            new_contract_ids = set()

            for item in items:
                contract_id = item["id"]
                print(item["contract_number"])
                if contract_id not in existing_contract_ids and contract_id not in new_contract_ids:
                    contract = Contract(
                        id=contract_id,
                        company=item["company"],
                        contract_number=item["contract_number"],
                        control_number=item["control_number"],
                        client_name=item["client_name"],
                        project_name=item["project_name"],
                        freight_estimated=item["freight_estimated"],
                    )
                    contracts_to_create.append(contract)
                    new_contract_ids.add(contract_id)

            with transaction.atomic():
                if contracts_to_create:
                    Contract.objects.bulk_create(contracts_to_create)

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
