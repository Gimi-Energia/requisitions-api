from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.models import User
from apps.users.serializers import UserSerializer


class UsersList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "email"]
    ordering_fields = ["name", "email", "type", "department"]
    permission_classes = [AllowAny]


class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
