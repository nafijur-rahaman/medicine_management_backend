from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    role = models.CharField(
        max_length=50,
        choices=[
            ('admin', 'Admin'),
            ('medicine_manager', 'Medicine Manager'),
            ('order_manager', 'Order Manager')
        ],
        default='medicine_manager'
    )
    email = models.EmailField(unique=True)
    image = CloudinaryField('image', default='dummyimage.jpg') 



    def __str__(self):
        return self.username
