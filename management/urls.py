from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, CategoryViewSet, MedicineViewSet, 
    MedicineStockViewSet, OrderViewSet
)

router = DefaultRouter()
router.register('customers', CustomerViewSet, basename='customer')
router.register('categories', CategoryViewSet, basename='category')
router.register('medicines', MedicineViewSet, basename='medicine')
router.register('stocks', MedicineStockViewSet, basename='stock')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
