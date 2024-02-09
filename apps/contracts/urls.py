from django.urls import path

from apps.contracts.views import ContractList, ContractDetail, ContractsDataAPIView

urlpatterns = [
    path("api/contracts/", ContractList.as_view(), name="contracts-list"),
    path("api/contracts/iapp/", ContractsDataAPIView.as_view(), name="contracts-iapp"),
    path("api/contracts/<str:pk>/", ContractDetail.as_view(), name="contract-detail"),
]
