from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.maintenances.models import Maintenance
from apps.maintenances.serializers import MaintenanceSerializer
from setup.validators.custom_view_validator import CustomErrorHandlerMixin

from .services.email_service import send_status_change_email


class MaintenanceList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
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


class MaintenanceDetail(CustomErrorHandlerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        old_status = serializer.instance.status

        with transaction.atomic():
            instance = serializer.save()

            if old_status != instance.status:
                if instance.status == "Scheduled" and not instance.forecast_date:
                    raise serializers.ValidationError(
                        "Para programar a requisição é necessário inserir a data de previsão"
                    )
                
                send_status_change_email(instance)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError as ve:
            return self.handle_validation_error(ve)
        except Exception as e:
            return self.handle_generic_exception(e, request)
