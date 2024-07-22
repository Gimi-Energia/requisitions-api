import os

from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from utils.permissions import IsAdminPost, IsAuthenticatedGet

from .services.iapp_service import get_iapp_products


class ProductsDataAPIView(APIView):
    def get(self, request):
        try:
            items = get_iapp_products()

            if not items:
                return Response(
                    {"message": "Error finding products"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            products_to_create = []
            existing_product_codes = set(
                Product.objects.filter(code__in=[item["code"] for item in items]).values_list(
                    "code", flat=True
                )
            )
            new_product_codes = set()

            for item in items:
                product_code = item["code"]
                print(product_code)
                if (
                    product_code not in existing_product_codes
                    and product_code not in new_product_codes
                ):
                    product = Product(
                        code=product_code,
                        id=item["id"],
                        un=item["un"],
                        description=item["description"],
                    )
                    products_to_create.append(product)
                    new_product_codes.add(product_code)

            with transaction.atomic():
                if products_to_create:
                    Product.objects.bulk_create(products_to_create)

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
    search_fields = ["code", "description"]
    ordering_fields = ["code", "un", "price"]
    filterset_fields = ["code", "description", "un"]

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


def remove_duplicates_view(request):
    duplicate_codes = (
        Product.objects.values("code").annotate(code_count=Count("id")).filter(code_count__gt=1)
    )

    for duplicate in duplicate_codes:
        products_to_delete_ids = Product.objects.filter(code=duplicate["code"]).values_list(
            "id", flat=True
        )[1:]

        if products_to_delete_ids:
            Product.objects.filter(id__in=list(products_to_delete_ids)).delete()

    return HttpResponse({"success": "Produtos duplicados removidos com sucesso."})
