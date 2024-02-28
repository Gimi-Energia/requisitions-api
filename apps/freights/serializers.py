from rest_framework import serializers

from apps.providers.models import Transporter
from apps.freights.models import Freight, FreightQuotation
from utils.validators.valid_date import retroactive_date


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
            "cte_number",
        )

    def validate(self, data):
        print(data)
        if data.get("request_date") and not retroactive_date(data["request_date"]):
            raise serializers.ValidationError(
                {"request_date": "A data da requisição não pode ser retroativa."}
            )
        if data.get("execution_date") and not retroactive_date(data["execution_date"]):
            raise serializers.ValidationError(
                {"execution_date": "A data da execução não pode ser retroativa."}
            )
        if data.get("approval_date") and not retroactive_date(data["approval_date"]):
            raise serializers.ValidationError(
                {"approval_date": "A data da aprovação não pode ser retroativa."}
            )

        return data

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
