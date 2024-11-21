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
        cost_center_id = self.kwargs['cost_center_id']
        cost_center = Department.objects.filter(id=cost_center_id)[0]
        return Position.objects.filter(cost_center = cost_center)