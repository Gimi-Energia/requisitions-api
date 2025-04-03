import json
from rest_framework import serializers

from apps.departments.serializers import DepartmentCustomSerializer
from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.purchases.models import Purchase, PurchaseProduct
from apps.users.serializers import UserCustomSerializer
from utils.validators.valid_date import retroactive_date


class PurchaseProductReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = PurchaseProduct
        fields = ("id", "uuid", "product", "quantity", "price", "status", "obs")


class PurchaseProductWriteSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=False
    )
    uuid = serializers.UUIDField(required=False)

    class Meta:
        model = PurchaseProduct
        fields = ("uuid", "product_id", "quantity", "price", "status", "obs")


class PurchaseReadSerializer(serializers.ModelSerializer):
    requester = UserCustomSerializer()
    approver = UserCustomSerializer()
    department = DepartmentCustomSerializer()
    products = PurchaseProductReadSerializer(many=True, source="purchaseproduct_set")

    class Meta:
        model = Purchase
        fields = "__all__"


class PurchaseWriteSerializer(serializers.ModelSerializer):
    products = PurchaseProductWriteSerializer(many=True, source="purchaseproduct_set")
    uuid = serializers.UUIDField(required=False)

    class Meta:
        model = Purchase
        fields = "__all__"

    def validate(self, data):
        if data.get("request_date") and not retroactive_date(data["request_date"]):
            raise serializers.ValidationError({"request_date": "Não é permitido data retroativa."})

        if data.get("quotation_date") and not data.get("quotation_emails"):
            raise serializers.ValidationError({"emails": "Deve ter no mínimo um fornecedor."})

        return data

    def create(self, validated_data):
        products_data = validated_data.pop("purchaseproduct_set")

        if len(products_data) == 0:
            raise serializers.ValidationError("Não é permitido requisição sem produtos.")

        # if len(set((product_data["product"],) for product_data in products_data)) != len(
        #     products_data
        # ):
        #     raise serializers.ValidationError({"products": "Não é permitido produtos repetidos."})

        purchase = Purchase.objects.create(**validated_data)

        for product_data in products_data:
            product = product_data["product"]
            quantity = product_data["quantity"]
            price = product_data["price"]
            status = product_data["status"]
            obs = product_data["obs"]
            PurchaseProduct.objects.create(
                purchase=purchase,
                product=product,
                quantity=quantity,
                price=price,
                status=status,
                obs=obs,
            )

        return purchase

    def update(self, instance, validated_data):
        products_data = validated_data.pop("purchaseproduct_set", None)

        if products_data:
            if hasattr(instance, "purchaseproduct_set"):
                for purchase_product in instance.purchaseproduct_set.all():
                    for product_data in products_data:
                        if "uuid" not in product_data:
                            raise serializers.ValidationError("UUID is required to update purchase products.")
                        status = product_data.get("status")
                        quantity = product_data.get("quantity")
                        price = product_data.get("price")
                        obs = product_data.get("obs")
                        
                        if purchase_product.uuid == product_data.get("uuid"):
                            if status and purchase_product.status != status:
                                purchase_product.status = status
                            if quantity and purchase_product.quantity != quantity:
                                purchase_product.quantity = quantity
                            if price and purchase_product.price != price:
                                purchase_product.price = price
                            if obs and purchase_product.obs != obs:
                                purchase_product.obs = obs

                            purchase_product.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
