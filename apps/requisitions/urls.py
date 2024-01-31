from django.urls import path
from apps.requisitions.views import (
    RequisitionListCreateView,
    RequisitionDetailView,
    RequisitionProductListCreateView,
)

urlpatterns = [
    path("api/requisitions/", RequisitionListCreateView.as_view(), name="requisition-list-create"),
    path("api/requisitions/<str:pk>/", RequisitionDetailView.as_view(), name="requisition-detail"),
    path(
        "api/requisitions/<str:pk>/products/",
        RequisitionProductListCreateView.as_view(),
        name="requisition-product-list-create",
    ),
]
