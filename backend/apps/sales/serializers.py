from rest_framework import serializers
from .models import Purchase, PurchaseItem, Sale, SaleItem, apply_purchase, apply_sale

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta: model=PurchaseItem; fields=["id","product","qty","unit_cost"]

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)
    class Meta: model=Purchase; fields=["id","supplier","notes","created_at","items"]
    def create(self, data):
        items = data.pop("items", [])
        po = Purchase.objects.create(**data)
        PurchaseItem.objects.bulk_create([PurchaseItem(purchase=po, **i) for i in items])
        apply_purchase(po)
        return po

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta: model=SaleItem; fields=["id","product","qty","unit_price"]

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    class Meta: model=Sale; fields=["id","customer_name","notes","created_at","items"]
    def create(self, data):
        items = data.pop("items", [])
        so = Sale.objects.create(**data)
        SaleItem.objects.bulk_create([SaleItem(sale=so, **i) for i in items])
        apply_sale(so)
        return so
