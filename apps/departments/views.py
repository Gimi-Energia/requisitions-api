from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from apps.departments.models import Department
from apps.departments.serializers import DepartmentSerializer
from utils.permissions import IsAdminPost, IsAuthenticatedGet

from django.db.models.functions import Length


class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.annotate(id_length=Length('id')).filter(id_length=7)
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "name"]
    ordering_fields = ["name"]
    filterset_fields = ["id", "name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedGet()]
        elif self.request.method == "POST":
            return [IsAdminPost()]
        return super().get_permissions()


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
