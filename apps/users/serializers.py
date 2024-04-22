from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.users.models import User
from apps.users.validators.api import (
    valid_email,
    valid_name,
    valid_password,
    equal_passwords,
    valid_phone,
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "type",
            "company",
            "department",
            "password",
            "password_confirm",
            "is_admin",
            "groups",
        )

    def validate(self, data):
        if not valid_name(data["name"]):
            raise serializers.ValidationError({"name": "Don't include numbers in this field!"})
        if not valid_email(data["email"]):
            raise serializers.ValidationError({"email": "Invalid email!"})
        if not valid_phone(data["phone"]):
            raise serializers.ValidationError(
                {"phone": "O número de celular deve seguir o padrão: (XX) 9XXXX-XXXX!"}
            )
        if not equal_passwords(data["password"], data["password_confirm"]):
            raise serializers.ValidationError({"password_confirm": "Password don't match"})
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
