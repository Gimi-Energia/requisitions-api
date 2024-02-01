from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User
from apps.users.serializers import UserSerializer
from utils.permissions import AllowAnyPost, IsAdminGet


class UsersList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["email", "type", "department__name", "is_admin"]
    ordering_fields = ["name", "email", "type", "department__name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminGet()]
        elif self.request.method == "POST":
            return [AllowAnyPost()]
        return super().get_permissions()


class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
