from django.db import models
from django.contrib.auth.models import User
import json

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('seed', 'Seed'),
        ('supply', 'Supply'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    stock = models.PositiveIntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    items = models.JSONField(default=list)  # JSON field to store order items
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    shipping_date = models.DateField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"




