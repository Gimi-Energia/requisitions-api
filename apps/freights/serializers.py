from rest_framework import serializers

from apps.providers.models import Transporter
from apps.freights.models import Freight, FreightQuotation


class FreightQuotationSerializer(serializers.ModelSerializer):
    transporter_id = serializers.PrimaryKeyRelatedField(
        queryset=Transporter.objects.all(), source="transporter", write_only=False
    )

    class Meta:
        model = FreightQuotation
        fields = ("transporter_id", "price", "status")


class FreightSerializer(serializers.ModelSerializer):
    quotations = FreightQuotationSerializer(many=True, source="freightquotation_set")

    class Meta:
        model = Freight
        fields = (
            "id",
            "company",
            "department",
            "request_date",
            "requester",
            "motive",
            "obs",
            "status",
            "quotations",
            "approver",
            "approval_date",
        )

    def create(self, validated_data):
        quotations_data = validated_data.pop("freightquotation_set")
        freight = Freight.objects.create(**validated_data)

        for quotation_data in quotations_data:
            transporter = quotation_data["transporter"]
            price = quotation_data["price"]
            status = quotation_data["status"]
            FreightQuotation.objects.create(
                freight=freight, transporter=transporter, price=price, status=status
            )

        return freight
