from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class PurchaseHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="history")
    total = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    orders_count = models.IntegerField(default=1)  # simplificado
