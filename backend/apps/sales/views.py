from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsSupervisorOrAdmin
from .models import Purchase, Sale
from .serializers import PurchaseSerializer, SaleSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.prefetch_related("items").all().order_by("-created_at")
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated & IsSupervisorOrAdmin]

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.prefetch_related("items").all().order_by("-created_at")
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated & IsSupervisorOrAdmin]
