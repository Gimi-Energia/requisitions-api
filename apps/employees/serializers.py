from rest_framework import serializers

from apps.employees.models import Position, Employee

from apps.departments.serializers import DepartmentSerializer
from apps.users.serializers import UserCustomSerializer


class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeReadSerializer(serializers.ModelSerializer):
    cost_center = DepartmentSerializer()
    requester = UserCustomSerializer()
    approver = UserCustomSerializer()

    class Meta:
        model = Employee
        fields = "__all__"
