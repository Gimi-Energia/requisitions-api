from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.freights.models import Freight, FreightQuotation
from apps.freights.serializers import FreightSerializer, FreightQuotationSerializer


class FreightListCreateView(generics.ListCreateAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []
    permission_classes = [IsAuthenticated]


class FreightDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        super().perform_update(serializer)
        new_instance = self.get_object()
        new_status = new_instance.status

        if old_status != "Pending" and new_status == "Pending":
            table_rows = []

            freight_pk = self.kwargs.get("pk")
            freight_quotations = FreightQuotation.objects.filter(freight=freight_pk)

            for freight_quotation in freight_quotations:
                if freight_quotation.status == "Approved":
                    transporter = freight_quotation.transporter.name
                    quotation_price = freight_quotation.price
                    table_row = f"<tr><td>{transporter}</td><td>R$ {quotation_price}</td></tr>"
                    table_rows.append(table_row)

            table_body = "".join(table_rows)

            table_html = f"""
            <table border="1">
                <tr>
                    <th>Transportadora</th>
                    <th>Preço</th>
                </tr>
                {table_body}
            </table>
            """

            subject = "Aprovação de Solicitação de Frete"
            html_message = f"""
            <html>
                <head>
                    <style>
                        * {'{ font-size: 1rem; }'}
                        table {{
                            border-collapse: collapse;
                        }}
                        th, td {{
                            border: 1px solid black;
                            padding: 5px;
                            text-align: left;
                            font-size: 0.9rem;
                        }}
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
                            <li>Data solicitada: 
                                {new_instance.request_date.strftime("%d/%m/%Y")}
                            </li>
                            <li>Motivo: {new_instance.motive}</li>
                            <li>Obsevações: {new_instance.obs}</li>
                            <li>Cotação: <br>{table_html}</li>
                        </ul>
                    </div>
                </body>
            </html>
            """

            send_mail(
                subject,
                "This is a plain text for email clients that don't support HTML",
                "dev2@engenhadev.com",
                [new_instance.requester.email],
                fail_silently=False,
                html_message=html_message,
            )

        return Response(status=status.HTTP_200_OK)


class FreightQuotationListCreateView(generics.ListCreateAPIView):
    serializer_class = FreightQuotationSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        freight_pk = self.kwargs["freight_pk"]
        return FreightQuotation.objects.filter(freight=freight_pk)
