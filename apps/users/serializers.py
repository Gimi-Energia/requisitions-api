from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.users.models import User
from apps.users.validators.api import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "password",
            "password_confirm",
        )

    def validate(self, data):
        if not valid_name(data["name"]):
            raise serializers.ValidationError(
                {"name": "Don't include numbers in this field!"}
            )
        if not valid_email(data["email"]):
            raise serializers.ValidationError({"email": "Invalid email!"})
        if not equal_passwords(data["password"], data["password_confirm"]):
            raise serializers.ValidationError(
                {"password_confirm": "Password don't match"}
            )
        if not valid_password(data["password"]):
            raise serializers.ValidationError(
                {
                    "password": "The password must have at least 8 characters, lowercase, uppercase, number and symbol"
                }
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user
