from django.urls import path

from apps.freights.views import (
    ExportFreightsView,
    FreightDetailView,
    FreightListCreateView,
    FreightQuotationListCreateView,
)

urlpatterns = [
    path("api/freights/", FreightListCreateView.as_view(), name="freight-list-create"),
    path("api/freights/export/", ExportFreightsView.as_view(), name="freight-export"),
    path("api/freights/<str:pk>/", FreightDetailView.as_view(), name="freight-detail"),
    path(
        "api/freights/<str:pk>/quotations/",
        FreightQuotationListCreateView.as_view(),
        name="freight-quotations-list-create",
    ),
]
