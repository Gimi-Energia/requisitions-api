from rest_framework import filters, generics, permissions
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User
from apps.users.serializers import UserSerializer


class AllowAnyPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class IsAdminGet(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class UsersList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "email"]
    ordering_fields = ["name", "email", "type", "department"]
    permission_classes = [AllowAnyPost]


class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
