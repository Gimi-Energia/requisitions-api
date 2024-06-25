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
        fields = "__all__"

    def validate(self, data):
        if data.get("request_date") and not retroactive_date(data["request_date"]):
            raise serializers.ValidationError({"request_date": "Não é permitido data retroativa."})

        return data

    def create(self, validated_data):
        quotations_data = validated_data.pop("freightquotation_set")
        is_internal = validated_data.get("is_internal", False)

        internal_transporter_count = sum(
            1 for q in quotations_data if q["transporter"].name == "FRETE INTERNO GRUPO GIMI"
        )

        external_transporter_count = sum(
            1 for q in quotations_data if q["transporter"].name != "FRETE INTERNO GRUPO GIMI"
        )

        if not is_internal and internal_transporter_count > 0:
            raise serializers.ValidationError(
                "Para 'FRETE INTERNO GRUPO GIMI', a requisição deve ser definida como INTERNA."
            )

        if is_internal:
            if len(quotations_data) != 1:
                raise serializers.ValidationError(
                    "Para frete interno, deve haver apenas uma transportadora."
                )

            quotation_data = quotations_data[0]
            transporter_name = quotation_data["transporter"].name
            transporter_status = quotation_data["status"]
            freight_status = validated_data["status"]

            if transporter_name != "FRETE INTERNO GRUPO GIMI":
                raise serializers.ValidationError(
                    "Para frete interno, a transportadora deve ser 'FRETE INTERNO GRUPO GIMI'."
                )

            if transporter_status != "Approved" or freight_status != "Approved":
                raise serializers.ValidationError(
                    "Para frete interno, os status devem ser APROVADO."
                )
        else:
            if internal_transporter_count > 0 and external_transporter_count > 0:
                raise serializers.ValidationError(
                    "Não é permitido incluir 'FRETE INTERNO GRUPO GIMI' junto com outras transportadoras."
                )

            if len(
                set((quotation_data["transporter"],) for quotation_data in quotations_data)
            ) != len(quotations_data):
                raise serializers.ValidationError(
                    {"quotations": "Não é permitido transportadoras repetidas."}
                )

            freight = Freight.objects.create(**validated_data)

            for quotation_data in quotations_data:
                transporter = quotation_data["transporter"]
                price = quotation_data["price"]
                status = quotation_data["status"]
                FreightQuotation.objects.create(
                    freight=freight,
                    transporter=transporter,
                    price=price,
                    status=status,
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
