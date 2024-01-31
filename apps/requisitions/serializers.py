from rest_framework import serializers
from .models import Requisition, RequisitionProduct
from apps.products.models import Product


class RequisitionProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=False
    )

    class Meta:
        model = RequisitionProduct
        fields = ("product_id", "quantity")


class RequisitionSerializer(serializers.ModelSerializer):
    products = RequisitionProductSerializer(many=True, source="requisitionproduct_set")

    class Meta:
        model = Requisition
        fields = ("id", "company", "date", "user", "motive", "obs", "is_approved", "products")

    def create(self, validated_data):
        products_data = validated_data.pop("requisitionproduct_set")
        requisition = Requisition.objects.create(**validated_data)

        for product_data in products_data:
            product = product_data["product"]
            quantity = product_data["quantity"]
            RequisitionProduct.objects.create(
                requisition=requisition, product=product, quantity=quantity
            )

        return requisition
