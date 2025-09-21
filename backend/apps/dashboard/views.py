from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.inventory.models import Product
from apps.sales.models import Sale, SaleItem

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def basic_metrics(request):
    today = timezone.now().date()
    daily_sales = (SaleItem.objects
                   .filter(sale__created_at__date=today)
                   .aggregate(total=Sum("unit_price")))
    top_products = (SaleItem.objects
                    .values("product__id","product__name")
                    .annotate(q=Sum("qty"))
                    .order_by("-q")[:5])
    low_stock = Product.objects.filter(active=True, stock__lte=models.F("min_stock")).values("id","name","stock","min_stock")
    return Response({
        "sales_today": daily_sales["total"] or 0,
        "top_products": list(top_products),
        "low_stock_alerts": list(low_stock),
    })
