from rest_framework import serializers

from apps.employees.models import Position, Employee

from apps.departments.serializers import DepartmentSerializer
from apps.users.serializers import UserCustomSerializer

from utils.validators.valid_date import retroactive_date


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

        if data.get("created_at") and not retroactive_date(data["created_at"]):
            raise serializers.ValidationError({"created_at": "Não é permitido data retroativa."})

        if data.get("start_date") and not retroactive_date(data["start_date"]):
            raise serializers.ValidationError({"start_date": "Não é permitido data retroativa."})

        return data



class EmployeeReadSerializer(serializers.ModelSerializer):
    position = PositionReadSerializer()
    cost_center = DepartmentSerializer()
    requester = UserCustomSerializer()
    approver = UserCustomSerializer()

    class Meta:
        model = Employee
        fields = "__all__"
