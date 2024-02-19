from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from apps.freights.models import Freight, FreightQuotation
from apps.freights.serializers import FreightSerializer, FreightQuotationSerializer


class FreightListCreateView(generics.ListCreateAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []
    # permission_classes = [IsAuthenticated]


class FreightDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer
    permission_classes = [IsAuthenticated]


class FreightQuotationListCreateView(generics.ListCreateAPIView):
    serializer_class = FreightQuotationSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        freight_pk = self.kwargs["freight_pk"]
        return FreightQuotation.objects.filter(freight=freight_pk)
