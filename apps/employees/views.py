from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend

from apps.departments.models import Department

from .models import Position, Employee
from .serializers import PositionsSerializer, EmployeeSerializer

# Create your views here.
class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class PositionList(generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company", "cost_center__id"]
    # permission_classes = [IsAuthenticated]
    
class EmployeeCreate(generics.CreateAPIView):
    model = Employee
    serializer_class = EmployeeSerializer

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [IsAuthenticated]