from django.urls import path

from .views import EmployeeList, PositionList, EmployeeCreate, EmployeeDetail

urlpatterns = [
    path("api/employees/", EmployeeList.as_view(), name="employees-list"),
    path("api/employees/position/", PositionList.as_view(), name="position-list"),
    path("api/employees/create/", EmployeeCreate.as_view(), name="employee-create"),
    path("api/employees/<str:pk>/", EmployeeDetail.as_view(), name="employee-detail"),
]