import uuid
from django.db import models
from django.contrib.auth.models import User

class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"
    SHIPPED = "SHIPPED", "Shipped"
    DELIVERED = "DELIVERED", "Delivered"


class Customer(User):
    uuid = models.UUIDField(
        unique=True, editable=False, primary_key=True, verbose_name="UUID"
    )
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if len(self.phone) < 10:
            raise ValueError("Phone number should be at least 10 digits")
        if self.phone[0] == "+":
            self.phone = self.phone[1:]
        if len(self.phone) == 10:
            self.phone = f"254{self.phone[1:]}"
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    uuid = models.UUIDField(unique=True, editable=False, verbose_name="UUID")

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class Session(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
