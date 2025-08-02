from django.contrib import admin
from .models import Product, CartItem , Order

# Register the Product model
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)