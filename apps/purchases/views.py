from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.purchases.models import Purchase, PurchaseProduct
from apps.purchases.serializers import (
    PurchaseProductReadSerializer,
    PurchaseProductWriteSerializer,
    PurchaseReadSerializer,
    PurchaseWriteSerializer,
)
from setup.validators.custom_view_validator import CustomErrorHandlerMixin

from .services.email_service import (
    send_generic_product_email,
    send_purchase_quotation_email,
    send_quotation_email_with_pdf,
    send_status_change_email,
)
from .services.omie_service import include_purchase_requisition


class PurchaseListCreateView(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = ["created_at", "approval_date"]
    filterset_fields = [
        # Campos do modelo Purchase
        "status",
        "company",
        "department__id",
        "department__name",
        "created_at",
        "request_date",
        "requester__id",
        "requester__email",
        "motive",
        "obs",
        "approver__id",
        "approver__email",
        "approval_date",
        "has_quotation",
        "quotation_emails",
        "quotation_date",
        "control_number",
        "motive_denied",
        # Campos do modelo PurchaseProduct (Relacionamento ManyToMany)
        "purchaseproduct__product__code",
        "purchaseproduct__product__description",
        "purchaseproduct__quantity",
        "purchaseproduct__price",
        "purchaseproduct__status",
        "purchaseproduct__obs",
    ]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PurchaseReadSerializer
        return PurchaseWriteSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()
            instance = serializer.instance

            if instance.status == "Quotation":
                send_purchase_quotation_email(instance)

            if instance.status == "Opened":
                send_status_change_email(instance)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as ve:
            return self.handle_validation_error(ve)
        except Exception as e:
            return self.handle_generic_exception(e, request)


class PurchaseDetailView(CustomErrorHandlerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PurchaseReadSerializer
        return PurchaseWriteSerializer

    def perform_update(self, serializer):
        old_status = serializer.instance.status
        old_quotation_emails = serializer.instance.quotation_emails

        with transaction.atomic():
            instance = serializer.save()

            if old_status != instance.status:
                if instance.status == "Approved":
                    omie = include_purchase_requisition(instance)

                    if omie is None:
                        send_generic_product_email(instance)
                        send_status_change_email(instance)
                        return

                    success = omie is not False

                    if not success:
                        raise serializers.ValidationError("Erro no Omie: Abra um chamado")
                    elif success and omie.status_code == 500:
                        raise serializers.ValidationError(
                            f"Erro {omie.status_code} do Omie: Produto não cadastrado"
                        )
                    elif success and omie.status_code == 403:
                        raise serializers.ValidationError(
                            f"Erro {omie.status_code} do Omie: Token inválido"
                        )
                    elif success and omie.status_code != 200:
                        raise serializers.ValidationError(
                            f"Erro {omie.status_code} do Omie: Requisição inválida"
                        )

                    send_status_change_email(instance)
                    return

                send_status_change_email(instance)

            if (
                instance.quotation_emails
                and old_quotation_emails != instance.quotation_emails
                and instance.status == "Quotation"
            ):
                send_quotation_email_with_pdf(instance)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError as ve:
            return self.handle_validation_error(ve)
        except Exception as e:
            return self.handle_generic_exception(e, request)


class PurchaseProductListCreateView(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PurchaseProductReadSerializer
        return PurchaseProductWriteSerializer

    def get_queryset(self):
        purchase_pk = self.kwargs["pk"]
        return PurchaseProduct.objects.filter(purchase=purchase_pk)


class PurchaseProductDetail(CustomErrorHandlerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseProduct.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PurchaseProductReadSerializer
        return PurchaseProductWriteSerializer
