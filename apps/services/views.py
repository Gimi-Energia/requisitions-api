from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.services.models import Service, ServiceType
from apps.services.serializers import ServiceSerializer, ServiceTypeSerializer

from .services.email_service import (
    send_quotation_email_with_pdf,
    send_service_quotation_email,
    send_status_change_email,
)


class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        new_instance = serializer.instance
        if new_instance.status == "Quotation":
            send_service_quotation_email(new_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        old_quotation_emails = instance.quotation_emails

        super().perform_update(serializer)
        new_instance = self.get_object()

        if old_status != new_instance.status:
            send_status_change_email(new_instance)

        if old_quotation_emails is None and new_instance.quotation_emails != "":
            send_quotation_email_with_pdf(new_instance)

        return Response(status=status.HTTP_200_OK)


class ServiceTypeList(generics.ListCreateAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []
    permission_classes = [IsAuthenticated]


class ServiceTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAuthenticated]
