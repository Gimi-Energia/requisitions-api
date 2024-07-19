from django.urls import path

from apps.products.views import ProductDetail, ProductList, ProductsDataAPIView, remove_duplicates_view

urlpatterns = [
    path("api/products/", ProductList.as_view(), name="products-list"),
    path("api/products/remove_duplicates/", remove_duplicates_view, name="remove-duplicates"),
    path("api/products/iapp/", ProductsDataAPIView.as_view(), name="products-iapp"),
    path("api/products/<str:pk>/", ProductDetail.as_view(), name="product-detail"),
]
