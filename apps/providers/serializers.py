from rest_framework import serializers

from apps.providers.models import Provider, Transporter


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class TransporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporter
        fields = "__all__"


class TransporterCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporter
        fields = ["id", "name"]
