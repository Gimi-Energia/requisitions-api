from django.urls import path

from .views import EmployeeList, PositionList

urlpatterns = [
    path("api/employees/", EmployeeList.as_view(), name="employees-list"),
    path("api/employees/position/<cost_center_id>/", PositionList.as_view(), name="position-list"),
]