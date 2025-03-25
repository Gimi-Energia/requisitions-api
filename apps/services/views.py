from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.services.models import Service, ServiceType
from apps.services.serializers import (
    ServiceReadSerializer,
    ServiceTypeSerializer,
    ServiceWriteSerializer,
)
from setup.validators.custom_view_validator import CustomErrorHandlerMixin

from .services.email_service import (
    send_quotation_email_with_pdf,
    send_service_quotation_email,
    send_status_change_email,
)


class ServiceList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Service.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = ["created_at", "approval_date_director"]
    filterset_fields = [
        "id",
        "company",
        "department__id",
        "department__name",
        "created_at",
        "request_date",
        "requester__id",
        "requester__email",
        "motive",
        "obs",
        "provider",
        "service__id",
        "service__description",
        "value",
        "status",
        "has_quotation",
        "quotation_emails",
        "quotation_date",
        "control_number",
        "motive_denied",
        "approver_director__id",
        "approver_director__email",
        "approval_date_director",
        "approver_manager__id",
        "approver_manager__email",
        "approval_date_manager",
    ]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ServiceReadSerializer
        return ServiceWriteSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()
            instance = serializer.instance

            if instance.status == "Quotation":
                send_service_quotation_email(instance)

            if instance.status == "Opened":
                send_status_change_email(instance)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as ve:
            return self.handle_validation_error(ve)
        except Exception as e:
            return self.handle_generic_exception(e, request)


class ServiceDetail(CustomErrorHandlerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ServiceReadSerializer
        return ServiceWriteSerializer

    def perform_update(self, serializer):
        old_status = serializer.instance.status
        old_quotation_emails = serializer.instance.quotation_emails

        with transaction.atomic():
            instance = serializer.save()

            if (
                old_status != instance.status
                and instance.status == "Approved"
                and not instance.approval_date_director
            ):
                raise serializers.ValidationError(
                    detail={
                        "error": "Para mandar o e-mail de aprovação é necessário uma data de aprovação válida."
                    }
                )  # noqa: E501

            if old_status != instance.status:
                send_status_change_email(instance)

            if old_quotation_emails is None and isinstance(instance.quotation_emails, str):
                send_quotation_email_with_pdf(instance)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError as ve:
            return self.handle_validation_error(ve)
        except Exception as e:
            return self.handle_generic_exception(e, request)


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
