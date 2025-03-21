from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Category, Medicine, MedicineStock, Order
from .serializers import ( CustomerSerializer, CategorySerializer, 
    MedicineSerializer, MedicineStockSerializer, OrderSerializer
)

# Customer ViewSet
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Medicine ViewSet
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


# Medicine Stock ViewSet
class MedicineStockViewSet(viewsets.ModelViewSet):
    queryset = MedicineStock.objects.all()
    serializer_class = MedicineStockSerializer


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

