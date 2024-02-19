import uuid
from django.db import models
from django.contrib.auth.models import User

from api.sms import SMS


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    SHIPPED = 'SHIPPED', 'Shipped'
    DELIVERED = 'DELIVERED', 'Delivered'


class Customer(User):
    uuid = models.UUIDField(unique=True, editable=False)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.uuid = self.uuid or uuid.uuid4()
        if(self.phone < 10):
            raise ValueError("Phone number should be 10 digits")
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        SMS().send(self.customer.phone[-10:], f"Your order with id {self.id} has been placed successfully.")
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
