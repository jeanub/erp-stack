from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import ReadOnlyOrSupervisorUp
from .models import Product, StockMovement
from .serializers import ProductSerializer, StockMovementSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated & ReadOnlyOrSupervisorUp]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name","sku"]
    ordering_fields = ["price","stock","created_at"]

class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.select_related("product").all().order_by("-created_at")
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
