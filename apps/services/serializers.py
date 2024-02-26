from rest_framework import serializers
from apps.services.models import Service, ServiceType
from utils.validators.valid_date import retroactive_date


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

    def validate(self, data):
        print(data)
        if data.get("request_date") and not retroactive_date(data["request_date"]):
            raise serializers.ValidationError(
                {"request_date": "A data da requisição não pode ser retroativa."}, 422
            )
        if data.get("execution_date") and not retroactive_date(data["execution_date"]):
            raise serializers.ValidationError(
                {"execution_date": "A data da execução não pode ser retroativa."}, 422
            )
        if data.get("approval_date") and not retroactive_date(data["approval_date"]):
            raise serializers.ValidationError(
                {"approval_date": "A data da aprovação não pode ser retroativa."}, 422
            )

        return data


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = "__all__"
