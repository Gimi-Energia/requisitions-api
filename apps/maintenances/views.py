from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.maintenances.models import Maintenance, Responsible
from apps.maintenances.serializers import (
    MaintenanceReadSerializer,
    MaintenanceWriteSerializer,
    ResponsibleSerializer,
)
from setup.validators.custom_view_validator import CustomErrorHandlerMixin

from .services.email_service import send_status_change_email


class MaintenanceList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Maintenance.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = ["created_at", "approval_date", "forecast_date", "end_date"]
    filterset_fields = [
        "id",
        "company",
        "name",
        "extension",
        "department__name",
        "department__id",
        "object",
        "url",
        "obs",
        "requester__id",
        "requester__email",
        "created_at",
        "request_date",
        "status",
        "approver__id",
        "approver__email",
        "forecast_date",
        "approver_obs",
        "approver_status",
        "end_date",
        "motive_denied",
    ]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MaintenanceReadSerializer
        return MaintenanceWriteSerializer

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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MaintenanceReadSerializer
        return MaintenanceWriteSerializer

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


class ResponsibleView(generics.RetrieveUpdateAPIView):
    serializer_class = ResponsibleSerializer

    def get_object(self):
        return Responsible.objects.first()
