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
        fields = ("transporter_id", "price", "status", "name_other")


class FreightSerializer(serializers.ModelSerializer):
    quotations = FreightQuotationSerializer(many=True, source="freightquotation_set")

    class Meta:
        model = Freight
        fields = "__all__"

    def validate(self, data):
        print(data)
        if data.get("request_date") and not retroactive_date(data["request_date"]):
            raise serializers.ValidationError(
                {"request_date": "A data da requisição não pode ser retroativa."}
            )

        return data

    def create(self, validated_data):
        quotations_data = validated_data.pop("freightquotation_set")

        if len(set((quotation_data["transporter"],) for quotation_data in quotations_data)) != len(
            quotations_data
        ):
            raise serializers.ValidationError(
                {"quotations": "Não é permitido transportadoras repetidas."}
            )

        if len(quotations_data) != 3:
            raise serializers.ValidationError(
                {"quotations": "A requisição de frete deve ter 3 transportadoras"}
            )

        freight = Freight.objects.create(**validated_data)

        for quotation_data in quotations_data:
            transporter = quotation_data["transporter"]
            price = quotation_data["price"]
            status = quotation_data["status"]
            name_other = quotation_data.get("name_other")
            FreightQuotation.objects.create(
                freight=freight,
                transporter=transporter,
                price=price,
                status=status,
                name_other=name_other,
            )

        return freight

    def update(self, instance, validated_data):
        quotations_data = validated_data.pop("freightquotation_set", None)

        if quotations_data:
            if hasattr(instance, "freightquotation_set"):
                for freight_quotation in instance.freightquotation_set.all():
                    for quotation_data in quotations_data:
                        status = quotation_data.get("status")
                        price = quotation_data.get("price")

                        if freight_quotation.transporter == quotation_data.get("transporter"):
                            if status and freight_quotation.status != status:
                                freight_quotation.status = status
                            if price and freight_quotation.price != price:
                                freight_quotation.price = price

                            freight_quotation.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
