from rest_framework import generics
from apps.departments.models import Department
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.departments.serializers import DepartmentSerializer


class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
