from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.freights.models import Freight, FreightQuotation
from apps.freights.serializers import FreightQuotationSerializer, FreightSerializer
from setup.validators.custom_view_validator import CustomErrorHandlerMixin

from .services.email_service import send_status_change_email


class FreightListCreateView(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()
            instance = serializer.instance

            if instance.status == "Opened":
                send_status_change_email(instance)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as ve:
            return self.handle_validation_error(ve)
        except Exception as e:
            return self.handle_generic_exception(e, request)


class FreightDetailView(CustomErrorHandlerMixin, generics.RetrieveUpdateDestroyAPIView):
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
        except serializers.ValidationError as ve:
            return self.handle_validation_error(ve)
        except Exception as e:
            return self.handle_generic_exception(e, request)


class FreightQuotationListCreateView(generics.ListCreateAPIView):
    serializer_class = FreightQuotationSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        freight_pk = self.kwargs["pk"]
        return FreightQuotation.objects.filter(freight=freight_pk)
