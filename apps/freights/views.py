import io
from datetime import date

from django.core.management import call_command
from django.db import transaction
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.freights.models import ExportLog, Freight, FreightQuotation
from apps.freights.serializers import (
    FreightQuotationReadSerializer,
    FreightQuotationWriteSerializer,
    FreightReadSerializer,
    FreightWriteSerializer,
)
from setup.validators.custom_view_validator import CustomErrorHandlerMixin

from .services.email_service import send_status_change_email


class FreightListCreateView(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Freight.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = ["created_at", "approval_date", "due_date"]
    filterset_fields = ["status"]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FreightReadSerializer
        return FreightWriteSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()
            instance = serializer.instance

            if instance.status == "Opened" or instance.status == "Approved":
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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FreightReadSerializer
        return FreightWriteSerializer

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
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FreightQuotationReadSerializer
        return FreightQuotationWriteSerializer

    def get_queryset(self):
        freight_pk = self.kwargs.get("pk")
        return FreightQuotation.objects.filter(freight=freight_pk)


class ExportFreightsView(CustomErrorHandlerMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description="Data de início no formato YYYY-MM-DD",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description="Data de término no formato YYYY-MM-DD",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        try:  # TODO: Discomment this block when tests end
            # last_export = ExportLog.objects.last()
            # if last_export and last_export.export_date == date.today():
            #     return HttpResponse(
            #         {"error": "A exportação só pode ser feita uma vez por dia."}, status=403
            #     )

            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            output = io.StringIO()
            call_command("exportfreights", start_date=start_date, end_date=end_date, stdout=output)

            ExportLog.objects.create()

            response = HttpResponse(output.getvalue(), content_type="text/csv")
            response["Content-Disposition"] = "attachment; filename=freights_export.csv"
            return response
        except Exception as e:
            return self.handle_generic_exception(e, request)
