from django.urls import path

from .views import EmployeeList, PositionList, EmployeeDetail, PositionDetail

urlpatterns = [
    path("api/employees/", EmployeeList.as_view(), name="employees-list"),
    path("api/employees/<str:pk>/", EmployeeDetail.as_view(), name="employee-detail"),
    path("api/employees/position/", PositionList.as_view(), name="position-list"),
    path("api/employees/position/<str:pk>", PositionDetail.as_view(), name="position-detail"),
]