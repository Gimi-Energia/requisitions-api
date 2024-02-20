from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.services.models import Service, ServiceType
from apps.services.serializers import ServiceSerializer, ServiceTypeSerializer


class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []
    permission_classes = [IsAuthenticated]


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        super().perform_update(serializer)
        new_instance = self.get_object()
        new_status = new_instance.status

        if old_status == "Approved" and new_status == "Approved":
            subject = "Aprovação de Solicitação de Serviço"
            html_message = f"""
            <html>
                <head>
                    <style>
                        * {'{ font-size: 1rem; }'}
                    </style>
                </head>
                <body>
                    <div>
                        <p>
                            Olá, {new_instance.requester.name}!
                            <br>
                            Sua solicitação foi aprovada por {new_instance.approver} 
                            em {new_instance.approval_date.strftime("%d/%m/%Y")}
                            <br>
                        </p>
                        <ul>
                            <p>Dados da solicitação:</p>
                            <li>Empresa: {new_instance.company}</li>
                            <li>Departamento: {new_instance.department}</li>
                            <li>Data da solicitação: 
                                {new_instance.request_date.strftime("%d/%m/%Y")}
                            </li>
                            <li>Motivo: {new_instance.motive}</li>
                            <li>Obsevações: {new_instance.obs}</li>
                            <li>Prestador: {new_instance.provider.name}</li>
                            <li>Serviço: {new_instance.service.description}</li>
                            <li>Valor: R$ {new_instance.value}</li>
                        </ul>
                    </div>
                </body>
            </html>
            """

            print(html_message)

            send_mail(
                subject,
                "This is a plain text for email clients that don't support HTML",
                "dev2@engenhadev.com",
                [new_instance.requester.email],
                fail_silently=False,
                html_message=html_message,
            )

        return Response(status=status.HTTP_200_OK)


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
