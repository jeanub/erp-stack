from django.db import transaction
from rest_framework import serializers

from .models import Purchase, PurchaseItem, Sale, SaleItem, apply_purchase, apply_sale


class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ["id", "product", "qty", "unit_cost"]


class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ["id", "supplier", "notes", "created_at", "items"]

    def create(self, validated_data):
        items = validated_data.pop("items", [])
        if not items:
            raise serializers.ValidationError({"items": ["At least one item is required."]})

        with transaction.atomic():
            purchase = Purchase.objects.create(**validated_data)
            purchase_items = [PurchaseItem(purchase=purchase, **item) for item in items]
            PurchaseItem.objects.bulk_create(purchase_items)
            apply_purchase(purchase)
        return purchase


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["id", "product", "qty", "unit_price"]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ["id", "customer_name", "notes", "created_at", "items"]

    def create(self, validated_data):
        items = validated_data.pop("items", [])
        if not items:
            raise serializers.ValidationError({"items": ["At least one item is required."]})

        try:
            with transaction.atomic():
                sale = Sale.objects.create(**validated_data)
                sale_items = [SaleItem(sale=sale, **item) for item in items]
                SaleItem.objects.bulk_create(sale_items)
                apply_sale(sale)
        except ValueError as exc:
            raise serializers.ValidationError({"items": [str(exc)]}) from exc
        return sale
