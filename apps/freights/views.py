from django.db import transaction
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
        old_status = serializer.instance.status

        with transaction.atomic():
            instance = serializer.save()

            if old_status != instance.status:
                send_status_change_email(instance)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FreightQuotationListCreateView(generics.ListCreateAPIView):
    serializer_class = FreightQuotationSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        freight_pk = self.kwargs["pk"]
        return FreightQuotation.objects.filter(freight=freight_pk)
