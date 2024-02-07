from django.urls import path
from apps.purchases.views import (
    PurchaseListCreateView,
    PurchaseDetailView,
    PurchaseProductListCreateView,
)

urlpatterns = [
    path("api/purchases/", PurchaseListCreateView.as_view(), name="purchase-list-create"),
    path("api/purchases/<str:pk>/", PurchaseDetailView.as_view(), name="purchase-detail"),
    path(
        "api/purchases/<str:pk>/products/",
        PurchaseProductListCreateView.as_view(),
        name="purchase-product-list-create",
    ),
]
