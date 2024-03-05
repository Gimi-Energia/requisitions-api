from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products.models import Product
from apps.purchases.models import Purchase, PurchaseProduct
from apps.purchases.serializers import PurchaseProductSerializer, PurchaseSerializer


class PurchaseListCreateView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    filterset_fields = []
    permission_classes = [IsAuthenticated]


class PurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        super().perform_update(serializer)
        new_instance = self.get_object()
        new_status = new_instance.status

        if old_status != "Approved" and new_status == "Approved":
            table_rows = []

            purchase_pk = self.kwargs.get("pk")
            purchase_products = PurchaseProduct.objects.filter(purchase=purchase_pk)

            for purchase_product in purchase_products:
                if purchase_product.status == "Approved":
                    product_code = purchase_product.product.code
                    product = Product.objects.filter(code=product_code).first()
                    product_description = product.description
                    product_quantity = purchase_product.quantity
                    product_price = purchase_product.price
                    table_row = f"<tr><td>{product_code}</td><td>{product_description}</td><td>{product_quantity}</td><td>R$ {product_price}</td></tr>"
                    table_rows.append(table_row)

            table_body = "".join(table_rows)

            table_html = f"""
            <table border="1">
                <tr>
                    <th>Código</th>
                    <th>Descrição</th>
                    <th>Quantidade</th>
                    <th>Preço Un.</th>
                </tr>
                {table_body}
            </table>
            """

            subject = "Aprovação de Solicitação de Compra"
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
                            <li>Produtos: <br>{table_html}</li>
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


class PurchaseProductListCreateView(generics.ListCreateAPIView):
    serializer_class = PurchaseProductSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = []
    ordering_fields = []
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        purchase_pk = self.kwargs["pk"]
        return PurchaseProduct.objects.filter(purchase=purchase_pk)
