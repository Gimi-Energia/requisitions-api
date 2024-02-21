from rest_framework import serializers

from apps.products.models import Product
from apps.purchases.models import Purchase, PurchaseProduct


class PurchaseProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=False
    )

    class Meta:
        model = PurchaseProduct
        fields = ("product_id", "quantity", "price", "status")


class PurchaseSerializer(serializers.ModelSerializer):
    products = PurchaseProductSerializer(many=True, source="purchaseproduct_set")

    class Meta:
        model = Purchase
        fields = (
            "id",
            "company",
            "department",
            "request_date",
            "requester",
            "motive",
            "obs",
            "status",
            "products",
            "approver",
            "approval_date",
        )

    def create(self, validated_data):
        products_data = validated_data.pop("purchaseproduct_set")
        purchase = Purchase.objects.create(**validated_data)

        for product_data in products_data:
            product = product_data["product"]
            quantity = product_data["quantity"]
            price = product_data["price"]
            status = product_data["status"]
            PurchaseProduct.objects.create(
                purchase=purchase, product=product, quantity=quantity, price=price, status=status
            )

        return purchase

    def update(self, instance, validated_data):
        products_data = validated_data.pop("purchaseproduct_set", None)

        if products_data:
            if hasattr(instance, "purchaseproduct_set"):
                for purchase_product in instance.purchaseproduct_set.all():
                    for product_data in products_data:
                        if purchase_product.product == product_data.get("product"):
                            if purchase_product.status != product_data.get("status"):
                                purchase_product.status = product_data.get("status")
                                purchase_product.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
