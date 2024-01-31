from rest_framework import generics
from apps.requisitions.models import Requisition, RequisitionProduct
from apps.requisitions.serializers import RequisitionSerializer, RequisitionProductSerializer


class RequisitionListCreateView(generics.ListCreateAPIView):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer


class RequisitionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer


class RequisitionProductListCreateView(generics.ListCreateAPIView):
    serializer_class = RequisitionProductSerializer

    def get_queryset(self):
        requisition_pk = self.kwargs["requisition_pk"]
        return RequisitionProduct.objects.filter(requisition=requisition_pk)
