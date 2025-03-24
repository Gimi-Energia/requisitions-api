from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.employees.models import Employee, Position, Software
from apps.employees.serializers import (
    EmployeeReadSerializer,
    EmployeeWriteSerializer,
    PositionWriteSerializer,
    SoftwareSerializer,
)
from apps.employees.services.email_service import send_status_change_email
from setup.validators.custom_view_validator import CustomErrorHandlerMixin


class EmployeeList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "company", "cost_center"]
    ordering_fields = ["created_at", "request_date", "approval_date", "start_date"]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployeeReadSerializer
        return EmployeeWriteSerializer

    def perform_create(self, serializer):
        print("vamos criar o Employee")
        with transaction.atomic():
            serializer.save()
            instance = serializer.instance
            print("Employee criado com sucesso")
            send_status_change_email(instance)


class EmployeeDetail(CustomErrorHandlerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployeeReadSerializer
        return EmployeeWriteSerializer

    def perform_update(self, serializer):
        print("preparando para atualizar...")
        old_status = serializer.instance.status
        print(f"status antigo {old_status}")

        with transaction.atomic():
            print("preparando para atualizar Employee")
            instance = serializer.save()
            print("Employee salvo com sucesso")

            if instance.status == "Approved" and not instance.complete_name:
                raise serializers.ValidationError(
                    detail={
                        "error": "Para mudar para aprovação é necessário inserir o nome completo do funcionário."
                    }
                )  # noqa: E501

            if old_status != instance.status:
                print("preparando para enviar o email")
                send_status_change_email(instance)


class PositionList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionWriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "id",
        "company",
        "cost_center__id",
        "cost_center__name",
        "request_date",
        "position__id",
        "position__name",
        "is_replacement",
        "has_pc",
        "needs_phone",
        "needs_tablet",
        "needs_software",
        "software_names",
        "has_workstation",
        "motive",
        "created_at",
        "requester__id",
        "requester__username",
        "status",
        "obs",
        "replaced_email",
        "complete_name",
        "start_date",
        "approver__id",
        "approver__username",
        "approval_date",
        "control_number",
        "motive_denied",
    ]
    permission_classes = [IsAuthenticated]


class PositionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionWriteSerializer


class SoftwareList(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    permission_classes = [IsAuthenticated]


class SoftwareDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    permission_classes = [IsAuthenticated]
