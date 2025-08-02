from django.urls import path
from .views import product_list, product_detail, add_to_cart, cart_view, update_cart, delete_cart_item 
from .views import checkout, payment_success, payment_cancel, order_detail, order_list, add_product, edit_product, delete_product

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'), 
    path('cart/', cart_view, name='cart_view'),
    path('update-cart/<int:item_id>/', update_cart, name='update_cart'), 
    path('delete-cart-item/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('checkout/', checkout, name='checkout'),
    path('success/', payment_success, name='payment_success'),
    path('cancel/', payment_cancel, name='payment_cancel'),
    path('orders/', order_list, name='order_list'), 
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    #### Superuser access
    path('add/', add_product, name='add_product'), 
    path('edit/<int:pk>/', edit_product, name='edit_product'), 
    path('delete/<int:pk>/', delete_product, name='delete_product'),
]
