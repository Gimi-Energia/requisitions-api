from rest_framework import generics, filters

from django_filters.rest_framework import DjangoFilterBackend

from setup.validators.custom_view_validator import CustomErrorHandlerMixin

from .models import Position, Employee
from .serializers import PositionsWriteSerializer, EmployeeReadSerializer, EmployeeWriteSerializer

# Create your views here.
class EmployeeList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status"]
    ordering_fields = ["created_at", "request_date", "approval_date", "start_date"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployeeReadSerializer
        return EmployeeWriteSerializer

class PositionList(generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionsWriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company", "cost_center__id"]
    # permission_classes = [IsAuthenticated]
    
class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeWriteSerializer
    # permission_classes = [IsAuthenticated]