from django.urls import path

from apps.services.views import ServiceDetail, ServiceList, ServiceTypeDetail, ServiceTypeList

urlpatterns = [
    path("api/services/", ServiceList.as_view(), name="services-list"),
    path("api/services/types/", ServiceTypeList.as_view(), name="services-type-list"),
    path("api/services/<str:pk>/", ServiceDetail.as_view(), name="services-detail"),
    path("api/services/types/<str:pk>/", ServiceTypeDetail.as_view(), name="services-ttpe-detail"),
]
