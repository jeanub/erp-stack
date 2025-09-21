from rest_framework import serializers
from .models import Product, StockMovement

class ProductSerializer(serializers.ModelSerializer):
    low_stock = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id","sku","name","price","stock","min_stock","active","low_stock","created_at"]
    def get_low_stock(self, obj): return obj.stock <= obj.min_stock

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ["id","product","kind","qty","ref","created_at"]
