from django.db import models
from users.models import CustomUser
from django.utils import timezone
# Create your models here.


# Medicine Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name

# Medicine Model
class Medicine(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Out of Stock', 'Out of Stock'),
    ]

    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='medicines')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    pack_size = models.CharField(max_length=50)
    total_pack = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return self.name

# Medicine Stock Model
class MedicineStock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='stocks')
    total_pack = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.medicine.total_pack += self.total_pack
        self.medicine.save()
        super().save(*args, **kwargs)

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address=models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
    
    
    
# Order Model

class Order(models.Model):
    order_no = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='orders')
    total_pack = models.PositiveIntegerField()
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')

    def save(self, *args, **kwargs):

        if not self.order_no:
            year_month = timezone.now().strftime('%Y%m')  
            last_order = Order.objects.filter(order_no__startswith=f"ORD{year_month}").last()
            new_id = int(last_order.order_no[6:]) + 1 if last_order else 1
            self.order_no = f"ORD{year_month}{new_id:04d}" 

    
        self.order_amount = self.medicine.unit_price * self.total_pack
        super().save(*args, **kwargs)
