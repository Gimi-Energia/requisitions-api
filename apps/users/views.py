from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User
from apps.users.serializers import UserSerializer
from utils.permissions import AllowAnyPost, IsAuthenticatedGet


class UsersList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = ["created_at", "approval_date"]
    filterset_fields = [
        "id",
        "name",
        "email",
        "phone",
        "type",
        "company",
        "department__id",
        "department__name",
        "is_active",
        "is_admin",
        "is_staff",
        "date_joined",
    ]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedGet()]
        elif self.request.method == "POST":
            return [AllowAnyPost()]
        return super().get_permissions()

    def sanitize_list_query_params(self, data: str):
        if data:
            return data.split(",")
        return data

    def filter_users(self):
        parameters = self.request.GET.dict()
        orderby_field = parameters.get("orderby")
        type = parameters.get("type", [])
        groups = parameters.get("groups")
        type = self.sanitize_list_query_params(type)

        if type:
            self.queryset = self.queryset.filter(type__in=type)
        if groups:
            self.queryset = self.queryset.filter(groups__id__in=groups)
        if orderby_field:
            self.queryset = self.queryset.order_by(orderby_field)

    def get(self, *args, **kwars):
        self.filter_users()
        return super().get(self.request, *args, **kwars)


class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
