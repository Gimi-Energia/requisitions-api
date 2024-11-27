from rest_framework import serializers

from apps.employees.models import Position, Employee

from apps.departments.serializers import DepartmentSerializer
from apps.users.serializers import UserCustomSerializer

from utils.validators.valid_date import retroactive_date

SOFTWARES = ("ZwCad", "Eplan P8", "Cogineer", "SolidWorks", "Metalix", "Inventor")


class PositionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class PositionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["id", "position"]


class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def validate(self, data):
        if data.get("request_date") and not retroactive_date(data["request_date"]):
            raise serializers.ValidationError({"request_date": "Não é permitido data retroativa."})

        if data.get("start_date") and not retroactive_date(data["start_date"]):
            raise serializers.ValidationError({"start_date": "Não é permitido data retroativa."})

        if data.get("approval_date") and not retroactive_date(data["approval_date"]):
            raise serializers.ValidationError({"approval_date": "Não é permitido data retroativa."})

        software_names = data.get("software_names").split(",")
        invalid_softwares = []
        print(software_names)

        for software_name in software_names:
            if software_name and SOFTWARES.count(software_name) == 0:
                invalid_softwares.append(software_name)

        print(invalid_softwares)
        if len(invalid_softwares) > 0:
            raise serializers.ValidationError(
                {"software_names": f"Os softwares {" ".join(invalid_softwares)} não são válidos."}
            )

        return data


class EmployeeReadSerializer(serializers.ModelSerializer):
    position = PositionReadSerializer()
    cost_center = DepartmentSerializer()
    requester = UserCustomSerializer()
    approver = UserCustomSerializer()

    class Meta:
        model = Employee
        fields = "__all__"
