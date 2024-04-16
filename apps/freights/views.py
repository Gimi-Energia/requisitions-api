from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.freights.models import Freight, FreightQuotation
from apps.freights.serializers import FreightQuotationSerializer, FreightSerializer

from .services.email_service import send_status_change_email


class FreightListCreateView(generics.ListCreateAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []
    permission_classes = [IsAuthenticated]


class FreightDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        
        super().perform_update(serializer)
        new_instance = self.get_object()
        freight_pk = self.kwargs.get("pk")

        if old_status != new_instance.status:
            send_status_change_email(new_instance, freight_pk)

        return Response(status=status.HTTP_200_OK)


class FreightQuotationListCreateView(generics.ListCreateAPIView):
    serializer_class = FreightQuotationSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        freight_pk = self.kwargs["pk"]
        return FreightQuotation.objects.filter(freight=freight_pk)
