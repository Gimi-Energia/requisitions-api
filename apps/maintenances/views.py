from django.db import transaction
from rest_framework import generics, serializers
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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MaintenanceReadSerializer
        return MaintenanceWriteSerializer

    def filter_maintenances(self):
        parameters = self.request.GET.dict()
        offset_min = int(parameters.get("offset-min", 0))
        offset_max = int(parameters.get("offset-max", 50))
        orderby_field = parameters.get("orderby")
        status = parameters.get("status")

        if status:
            self.queryset = self.queryset.filter(status=status)
        if orderby_field:
            self.queryset = self.queryset.order_by(orderby_field)

        self.queryset = self.queryset[offset_min:offset_max]

    def get(self, *args, **kwars):
        self.filter_maintenances()
        return super().get(self.request, *args, **kwars)

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
