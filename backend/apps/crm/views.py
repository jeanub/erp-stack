from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import ReadOnlyOrSupervisorUp
from .models import Customer, PurchaseHistory
from .serializers import CustomerSerializer, PurchaseHistorySerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by("-created_at")
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated & ReadOnlyOrSupervisorUp]

class PurchaseHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PurchaseHistory.objects.select_related("customer").all().order_by("-date")
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAuthenticated]
