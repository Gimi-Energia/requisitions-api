from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from apps.requisitions.models import Requisition, RequisitionProduct
from apps.requisitions.serializers import RequisitionSerializer, RequisitionProductSerializer


class RequisitionListCreateView(generics.ListCreateAPIView):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["company", "date", "user__id", "motive", "is_approved"]
    ordering_fields = ["date", "user__id", "motive", "is_approved"]
    filterset_fields = ["company", "date", "user__id", "is_approved"]
    permission_classes = [IsAuthenticated]


class RequisitionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    permission_classes = [IsAuthenticated]


class RequisitionProductListCreateView(generics.ListCreateAPIView):
    serializer_class = RequisitionProductSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        requisition_pk = self.kwargs["requisition_pk"]
        return RequisitionProduct.objects.filter(requisition=requisition_pk)
