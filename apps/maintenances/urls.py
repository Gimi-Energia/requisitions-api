from django.urls import path

from apps.maintenances.views import MaintenanceList, MaintenanceDetail

urlpatterns = [
    path("api/maintenances/", MaintenanceList.as_view(), name="maintenances-list"),
    path("api/maintenances/<str:pk>/", MaintenanceDetail.as_view(), name="maintenances-detail"),
]
