from django.db import models, transaction
from django.utils import timezone
from apps.inventory.models import Product, adjust_stock

class Purchase(models.Model):  # Entrada de stock
    created_at = models.DateTimeField(default=timezone.now)
    supplier = models.CharField(max_length=160, blank=True)
    notes = models.TextField(blank=True)

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)

class Sale(models.Model):  # Salida de stock
    created_at = models.DateTimeField(default=timezone.now)
    customer_name = models.CharField(max_length=160, blank=True)
    notes = models.TextField(blank=True)

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

def apply_purchase(purchase:Purchase):
    with transaction.atomic():
        for it in purchase.items.all():
            adjust_stock(it.product_id, +it.qty, ref=f"PO-{purchase.id}")

def apply_sale(sale:Sale):
    with transaction.atomic():
        for it in sale.items.all():
            adjust_stock(it.product_id, -it.qty, ref=f"SO-{sale.id}")
