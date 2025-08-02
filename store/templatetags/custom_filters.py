from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def sum_cart_total(cart_items):
    return sum(item.quantity * item.product.price for item in cart_items)
