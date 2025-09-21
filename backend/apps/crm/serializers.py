from rest_framework import serializers
from .models import Customer, PurchaseHistory

class CustomerSerializer(serializers.ModelSerializer):
    class Meta: model=Customer; fields=["id","name","email","phone","created_at"]

class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta: model=PurchaseHistory; fields=["id","customer","total","date","orders_count"]
