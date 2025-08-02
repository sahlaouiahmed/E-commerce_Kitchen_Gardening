from django.shortcuts import render, get_object_or_404 ,redirect,reverse
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ShippingForm , ProductForm
import stripe
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def product_list(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    category = request.GET.get('category', 'all')
    if category != 'all':
        products = products.filter(category__iexact=category)
    context = {
        'products': products,
        'category': category,
        'query': query,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]  # Fetch related products from the same category, exclude the current product, limit to 4
    return render(request, 'store/product_detail.html', {'product': product, 'related_products': related_products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock > 0:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        product.stock -= 1
        product.save()
        messages.success(request, f'{product.name} has been added to your cart successfully!')
    else:
        messages.error(request, 'Sorry, this product is out of stock.')
    return redirect('product_list')



@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'cart_items': cart_items})

@login_required
def update_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity > cart_item.product.stock:
            messages.error(request, f"Only {cart_item.product.stock} items available in stock.")
        elif quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    return redirect('cart_view')



@login_required
def delete_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart_view')


stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']
            
            amount = int(sum(item.quantity * item.product.price for item in cart_items) * 100)
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': amount,
                        'product_data': {
                            'name': 'Order from Kitchen Garden'
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
            )
            request.session['checkout_data'] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'address': address,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'amount': amount / 100
            }
            return redirect(session.url)
    else:
        form = ShippingForm()

    context = {
        'cart_items': cart_items,
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'store/checkout.html', context)




stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')
    checkout_data = request.session.pop('checkout_data', None)  # Pop to ensure it's only used once

    if session_id and checkout_data:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            delivery_cost = 0.00  # Free shipping for now
            shipping_date = datetime.now() + timedelta(days=5)  # Shipping date 5 days from now

            order_items = [
                {"product_id": item.product.id, "quantity": item.quantity}
                for item in CartItem.objects.filter(user=request.user)
            ]
            total_amount_with_delivery = checkout_data['amount'] + delivery_cost  # Add delivery cost to total amount

            order = Order.objects.create(
                user=request.user,
                first_name=checkout_data['first_name'],
                last_name=checkout_data['last_name'],
                email=checkout_data['email'],
                address=checkout_data['address'],
                city=checkout_data['city'],
                state=checkout_data['state'],
                zip_code=checkout_data['zip_code'],
                items=order_items,
                total_amount=total_amount_with_delivery,
                delivery_cost=delivery_cost,
                shipping_date=shipping_date
            )

            CartItem.objects.filter(user=request.user).delete()

            detailed_order_items = []
            for item in order.items:
                product = get_object_or_404(Product, id=item['product_id'])
                detailed_order_items.append({
                    'product': product,
                    'quantity': item['quantity']
                })

            # Prepare email content
            email_subject = f"Order Confirmation - {order.id}"
            email_body = f"""
            Thank you for your order, {order.first_name}!

            Order Number: {order.id}
            Date: {order.created_at}
            Total Amount: ${order.total_amount}
            Delivery Cost: ${order.delivery_cost}
            Shipping Date: {order.shipping_date}

            Shipping Address:
            {order.first_name} {order.last_name}
            {order.address}
            {order.city}, {order.state} {order.zip_code}

            Items:
            """
            for item in detailed_order_items:
                email_body += f"""
                - {item['product'].name}
                  Price: ${item['product'].price}
                  Quantity: {item['quantity']}
                """

            # Send confirmation email
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
                fail_silently=False,
            )

            return render(request, 'store/payment_success.html', {'order': order, 'order_items': detailed_order_items})

    return redirect('checkout')


@login_required
def payment_cancel(request):
    # Render the cancel page
    return render(request, 'store/cancel.html')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = []
    for item in order.items:
        product = get_object_or_404(Product, id=item['product_id'])
        order_items.append({
            'product': product,
            'quantity': item['quantity']
        })
    return render(request, 'store/order_detail.html', {'order': order, 'order_items': order_items})




#SUPERUSER 
def superuser_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


@superuser_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})



@superuser_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

@superuser_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'store/confirm_delete.html', {'product': product})
