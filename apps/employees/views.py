from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from apps.employees.models import Employee, Position
from apps.employees.serializers import (
    EmployeeReadSerializer,
    EmployeeWriteSerializer,
    PositionWriteSerializer,
)
from setup.validators.custom_view_validator import CustomErrorHandlerMixin


class EmployeeList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status"]
    ordering_fields = ["created_at", "request_date", "approval_date", "start_date"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployeeReadSerializer
        return EmployeeWriteSerializer


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployeeReadSerializer
        return EmployeeWriteSerializer


class PositionList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionWriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company", "cost_center__id"]
    # permission_classes = [IsAuthenticated]


class PositionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionWriteSerializer
