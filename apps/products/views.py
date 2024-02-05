from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from utils.permissions import IsAdminPost, IsAuthenticatedGet


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
