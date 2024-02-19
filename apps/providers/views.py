from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from apps.providers.models import Provider, Transporter
from apps.providers.serializers import ProviderSerializer, TransporterSerializer
from utils.permissions import IsAdminPost, IsAuthenticatedGet


class ProviderList(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedGet()]
        elif self.request.method == "POST":
            return [IsAdminPost()]
        return super().get_permissions()


class ProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]


class TransporterList(generics.ListCreateAPIView):
    queryset = Transporter.objects.all()
    serializer_class = TransporterSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedGet()]
        elif self.request.method == "POST":
            return [IsAdminPost()]
        return super().get_permissions()


class TransporterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transporter.objects.all()
    serializer_class = TransporterSerializer
    permission_classes = [IsAuthenticated]
