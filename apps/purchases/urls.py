from django.urls import path

from apps.purchases.views import (
    PurchaseDetailView,
    PurchaseFlowView,
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
        "api/purchases/flow/webhook/",
        PurchaseFlowView.as_view({"post": "webhook"}),
        name="purchase-flow-webhook",
    ),
    path(
        "api/purchases/<str:pk>/flow/",
        PurchaseFlowView.as_view({"get": "flow"}),
        name="purchase-flow",
    ),
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
