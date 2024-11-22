from django.urls import path

from .views import EmployeeList, PositionList, CreateEmployee

urlpatterns = [
    path("api/employees/", EmployeeList.as_view(), name="employees-list"),
    path("api/employees/position/<cost_center_id>/", PositionList.as_view(), name="position-list"),
    path("api/employees/create/", CreateEmployee.as_view(), name="create-employee"),
]