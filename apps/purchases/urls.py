from django.urls import path

from apps.purchases.views import (
    PurchaseDetailView,
    PurchaseListCreateView,
    PurchaseProductDetail,
    PurchaseProductListCreateView,
    UpdateSearchSaleOrderView,
)

urlpatterns = [
    path("api/purchases/", PurchaseListCreateView.as_view(), name="purchase-list-create"),
    path("api/purchases/search-omie/", UpdateSearchSaleOrderView.as_view(), name="search-omie"),
    path("api/purchases/<str:pk>/", PurchaseDetailView.as_view(), name="purchase-detail"),
    path(
        "api/purchases/<str:pk>/products/",
        PurchaseProductListCreateView.as_view(),
        name="purchase-product-list-create",
    ),
    path(
        "api/purchases/<str:pk>/products/<str:product_pk>/",
        PurchaseProductDetail.as_view(),
        name="purchase-product-list-create",
    ),
]
