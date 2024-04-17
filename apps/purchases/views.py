from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.purchases.models import Purchase, PurchaseProduct
from apps.purchases.serializers import PurchaseProductSerializer, PurchaseSerializer

from .services.email_service import (
    send_purchase_quotation_email,
    send_quotation_email_with_pdf,
    send_status_change_email,
)
from .services.omie_service import include_purchase_requisition


class PurchaseListCreateView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        new_instance = serializer.instance
        if new_instance.status == "Quotation":
            send_purchase_quotation_email(new_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        old_quotation_emails = instance.quotation_emails

        super().perform_update(serializer)
        new_instance = self.get_object()

        if old_status != new_instance.status:
            send_status_change_email(new_instance)

            if new_instance.status == "Approved":
                include_purchase_requisition(new_instance)

        if old_quotation_emails is None and isinstance(new_instance.quotation_emails, str):
            send_quotation_email_with_pdf(new_instance)

        return Response(status=status.HTTP_200_OK)


class PurchaseProductListCreateView(generics.ListCreateAPIView):
    serializer_class = PurchaseProductSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        purchase_pk = self.kwargs["pk"]
        return PurchaseProduct.objects.filter(purchase=purchase_pk)
