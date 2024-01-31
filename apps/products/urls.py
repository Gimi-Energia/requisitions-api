from django.urls import path

from apps.products.views import ProductList, ProductDetail

urlpatterns = [
    path("api/products/", ProductList.as_view(), name="products-list"),
    path("api/products/<str:pk>/", ProductDetail.as_view(), name="product-detail"),
]
