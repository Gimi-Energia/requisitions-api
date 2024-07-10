from django.urls import path

from apps.maintenances.views import MaintenanceDetail, MaintenanceList, ResponsibleView

urlpatterns = [
    path("api/maintenances/", MaintenanceList.as_view(), name="maintenances-list"),
    path(
        "api/maintenances/responsible/", ResponsibleView.as_view(), name="maintenances-responsible"
    ),
    path("api/maintenances/<str:pk>/", MaintenanceDetail.as_view(), name="maintenances-detail"),
]
