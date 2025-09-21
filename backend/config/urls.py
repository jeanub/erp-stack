from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.core.views import health
from apps.users.views import UserViewSet
from apps.inventory.views import ProductViewSet, StockMovementViewSet
from apps.sales.views import PurchaseViewSet, SaleViewSet
from apps.crm.views import CustomerViewSet, PurchaseHistoryViewSet
from apps.dashboard.views import basic_metrics

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"stock-movements", StockMovementViewSet, basename="stock-movement")
router.register(r"purchases", PurchaseViewSet, basename="purchase")
router.register(r"sales", SaleViewSet, basename="sale")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"purchase-history", PurchaseHistoryViewSet, basename="purchase-history")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/dashboard/basic/", basic_metrics),
    path("api/", include(router.urls)),
]
