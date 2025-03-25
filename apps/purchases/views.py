from datetime import datetime, timedelta

from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.purchases.models import Purchase, PurchaseFlow, PurchaseProduct
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
from .services.omie_service import (
    include_purchase_requisition,
    query_purchase_order,
    search_sale_orders,
)


class PurchaseListCreateView(CustomErrorHandlerMixin, generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = ["created_at", "approval_date_director"]
    filterset_fields = [
        "id",
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
        "approver_director__email",
        "approver_director__id",
        "approval_date_director",
        "has_quotation",
        "quotation_emails",
        "quotation_date",
        "control_number",
        "motive_denied",
        "quotation_link",
        "approver_manager__id",
        "approver_manager__email",
        "approval_date_manager",
        "omie_total",
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
                send_status_change_email(instance)

                if instance.status == "Approved":
                    omie = include_purchase_requisition(instance)

                    if omie is None:
                        send_generic_product_email(instance)
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

            if instance.quotation_emails and old_quotation_emails != instance.quotation_emails:
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


class UpdateSearchSaleOrderView(CustomErrorHandlerMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            search_sale_orders()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return self.handle_generic_exception(e, request)


class PurchaseFlowView(CustomErrorHandlerMixin, viewsets.ViewSet):
    @action(detail=True, methods=["get"])
    def flow(self, request, pk=None):
        try:
            purchase = Purchase.objects.get(pk=pk)
            purchase_flow, created = PurchaseFlow.objects.get_or_create(purchase=purchase)
            if created:
                purchase_flow.requested_date = purchase.request_date
                purchase_flow.approved_manager_date = purchase.approval_date_manager
                purchase_flow.approved_director_date = purchase.approval_date_director
                purchase_flow.save()
            return Response(purchase_flow, status=status.HTTP_200_OK)
        except Purchase.DoesNotExist:
            return Response({"detail": "Purchase not found."}, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=["post"])
    def webhook(self, request):
        try:
            data = request.data
            omie_data = data.get("event", {}).get("cabecalho_consulta", {})
            int_order = omie_data.get("cCodIntPed", "")

            if int_order.startswith("INT-"):
                control_number = int(int_order.split("-")[1])
                purchase = Purchase.objects.get(control_number=control_number)
                purchase_flow, created = PurchaseFlow.objects.get_or_create(purchase=purchase)
                omie_step = omie_data.get("cEtapa", "")
                date = datetime.now().date()

                if omie_step == "10":
                    if created:
                        purchase_flow.requested_date = purchase.request_date
                        purchase_flow.approved_manager_date = purchase.approval_date_manager
                        purchase_flow.approved_director_date = purchase.approval_date_director

                    purchase_flow.order_number = omie_data.get("cNumero", None)
                    purchase_flow.arrival_forecast_date = datetime.strptime(
                        omie_data.get("dDtPrevisao", None), "%d/%m/%Y"
                    ).date()
                    purchase_flow.step = "Ordered"
                elif omie_step == "15":
                    purchase_flow.purchased_date = date
                    purchase_flow.step = "Purchased"

                purchase_flow.save()

            return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
