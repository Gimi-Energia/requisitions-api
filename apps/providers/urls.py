from django.urls import path

from apps.providers.views import ProviderDetail, ProviderList, TransporterDetail, TransporterList

urlpatterns = [
    path("api/providers/", ProviderList.as_view(), name="providers-list"),
    path("api/providers/<str:pk>/", ProviderDetail.as_view(), name="provider-detail"),
    path("api/transporters/", TransporterList.as_view(), name="transporters-list"),
    path("api/transporters/<str:pk>/", TransporterDetail.as_view(), name="transporter-detail"),
]
