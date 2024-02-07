from django.urls import path

from apps.providers.views import ProviderList, ProviderDetail

urlpatterns = [
    path("api/providers/", ProviderList.as_view(), name="providers-list"),
    path("api/providers/<str:pk>/", ProviderDetail.as_view(), name="provider-detail"),
]
