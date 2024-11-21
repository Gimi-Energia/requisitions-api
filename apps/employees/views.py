from rest_framework import generics

from apps.departments.models import Department

from .models import Position
from .serializers import PositionsSerializer

# Create your views here.
class EmployeeList(generics.CreateAPIView):
    pass

class PositionList(generics.ListAPIView):
    serializer_class = PositionsSerializer

    def get_queryset(self):
        department_id = self.kwargs['department_id']
        department = Department.objects.filter(id=department_id)[0]
        return Position.objects.filter(department = department)