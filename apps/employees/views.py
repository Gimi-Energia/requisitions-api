from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend

from setup.validators.custom_view_validator import CustomErrorHandlerMixin

from .models import Position, Employee
from .serializers import PositionsSerializer, EmployeeReadSerializer, EmployeeWriteSerializer

# Create your views here.
class EmployeeList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]
    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployeeReadSerializer
        return EmployeeWriteSerializer

class PositionList(generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company", "cost_center__id"]
    # permission_classes = [IsAuthenticated]
    
class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeWriteSerializer
    # permission_classes = [IsAuthenticated]