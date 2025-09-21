from django.db import models, transaction

class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=160)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class StockMovement(models.Model):
    INBOUND="IN"; OUTBOUND="OUT"
    KIND_CHOICES=[(INBOUND,"Entrada"),(OUTBOUND,"Salida")]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    kind = models.CharField(max_length=3, choices=KIND_CHOICES)
    qty = models.IntegerField()
    ref = models.CharField(max_length=64, blank=True)  # id de compra/venta
    created_at = models.DateTimeField(auto_now_add=True)

def adjust_stock(product_id:int, delta:int, ref:str=""):
    from .models import Product, StockMovement
    with transaction.atomic():
        p = Product.objects.select_for_update().get(pk=product_id)
        new_stock = p.stock + delta
        if new_stock < 0:
            raise ValueError("Stock insuficiente")
        p.stock = new_stock
        p.save(update_fields=["stock"])
        StockMovement.objects.create(
            product=p,
            kind=StockMovement.INBOUND if delta>0 else StockMovement.OUTBOUND,
            qty=abs(delta),
            ref=ref
        )
        return p.stock
