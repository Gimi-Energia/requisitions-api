from django.urls import path

from apps.employees.views import (
    EmployeeDetail,
    EmployeeList,
    PositionDetail,
    PositionList,
    SoftwareDetail,
    SoftwareList,
)

urlpatterns = [
    path("api/employees/", EmployeeList.as_view(), name="employee-list"),
    path("api/employees/positions/", PositionList.as_view(), name="position-list"),
    path("api/employees/softwares/", SoftwareList.as_view(), name="software-list"),
    path("api/employees/positions/<str:pk>/", PositionDetail.as_view(), name="position-detail"),
    path("api/employees/softwares/<str:pk>/", SoftwareDetail.as_view(), name="software-detail"),
    path("api/employees/<str:pk>/", EmployeeDetail.as_view(), name="employee-detail"),
]
