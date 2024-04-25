import os

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
        token = str(os.getenv("TOKEN_GIMI"))
        secret = str(os.getenv("SECRET_GIMI"))

        try:
            items = get_iapp_products(token, secret)

            if not items:
                return Response(
                    {"message": "Error finding products"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            for item in items:
                product_code = item["code"]
                product, created = Product.objects.get_or_create(
                    code=product_code,
                    defaults={
                        "id": item["id"],
                        "un": item["un"],
                        "description": item["description"],
                    },
                )

                if not created:
                    product.un = item["un"]
                    product.description = item["description"]
                    product.save()

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
