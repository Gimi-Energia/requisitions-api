from django.urls import path

from views import EmployeeList

urlpatterns = [
    path("api/employees/", EmployeeList.as_view(), name="employees-list"),
]