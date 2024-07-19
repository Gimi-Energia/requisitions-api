from django.urls import path

from apps.departments.views import DepartmentDetail, DepartmentList

urlpatterns = [
    path("api/departments/", DepartmentList.as_view(), name="departments-list"),
    path("api/departments/<str:pk>/", DepartmentDetail.as_view(), name="departments-detail"),
]
