from django.urls import path
from apps.freights.views import (
    FreightListCreateView,
    FreightDetailView,
    FreightQuotationListCreateView,
)

urlpatterns = [
    path("api/freights/", FreightListCreateView.as_view(), name="freight-list-create"),
    path("api/freights/<str:pk>/", FreightDetailView.as_view(), name="freight-detail"),
    path(
        "api/freights/<str:pk>/quotations/",
        FreightQuotationListCreateView.as_view(),
        name="freight-quotations-list-create",
    ),
]
