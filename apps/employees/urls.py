from django.urls import path

from apps.employees.views import EmployeeDetail, EmployeeList, PositionDetail, PositionList

urlpatterns = [
    path("api/employees/", EmployeeList.as_view(), name="employees-list"),
    path("api/employees/positions/", PositionList.as_view(), name="position-list"),
    path("api/employees/<str:pk>/", EmployeeDetail.as_view(), name="employee-detail"),
    path("api/employees/positions/<str:pk>", PositionDetail.as_view(), name="position-detail"),
]
