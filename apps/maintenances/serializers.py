from rest_framework import serializers

from apps.departments.serializers import DepartmentCustomSerializer
from apps.maintenances.models import Maintenance, Responsible
from apps.users.serializers import UserCustomSerializer
from utils.validators.valid_date import retroactive_date


class MaintenanceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = "__all__"

    def validate(self, data):
        if data.get("request_date") and not retroactive_date(data["request_date"]):
            raise serializers.ValidationError({"request_date": "Não é permitido data retroativa."})

        if data.get("forecast_date") and not retroactive_date(data["forecast_date"]):
            raise serializers.ValidationError({"forecast_date": "Não é permitido data retroativa."})

        return data


class MaintenanceReadSerializer(serializers.ModelSerializer):
    requester = UserCustomSerializer()
    approver = UserCustomSerializer()
    department = DepartmentCustomSerializer()

    class Meta:
        model = Maintenance
        fields = "__all__"


class ResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsible
        fields = ["name", "email", "phone", "extension"]
