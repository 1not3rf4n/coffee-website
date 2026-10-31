import uuid
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.cart.cart import Cart
from apps.orders.models import Order, OrderItem
from apps.shop.models import Product

def checkout_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "سبد خرید شما خالی است!")
        return redirect('shop:index')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        order_number = f"NC-{random.randint(10000, 99999)}"
        order = Order.objects.create(
            order_number=order_number,
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=cart.get_total_price(),
            status='pending'
        )

        for item in cart:
            try:
                product = Product.objects.get(id=item['product_id'])
            except Product.DoesNotExist:
                product = None

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=item['title'],
                price=item['price'],
                quantity=item['quantity'],
                grind_type=item.get('grind_type', 'دانه کامل')
            )

        cart.clear()
        return redirect('orders:payment_mock', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})

def payment_mock_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/payment_mock.html', {'order': order})

def payment_verify_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    action = request.GET.get('action', 'success')

    if action == 'success':
        order.status = 'paid'
        order.tracking_code = f"TRK-{random.randint(100000, 999999)}"
        order.save()
        for item in order.items.all():
            if item.product:
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()
        messages.success(request, "پرداخت با موفقیت انجام شد!")
        return redirect('orders:order_success', order_id=order.id)
    else:
        order.status = 'cancelled'
        order.save()
        messages.error(request, "پرداخت توسط کاربر لغو گردید.")
        return render(request, 'orders/payment_failed.html', {'order': order})

def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


# Ordered pipeline the progress bar walks through (cancelled is handled apart).
TRACK_STEPS = [
    ('pending',    'ثبت سفارش',      'fa-file-invoice'),
    ('paid',       'پرداخت شد',       'fa-credit-card'),
    ('processing', 'برشته‌کاری',       'fa-fire'),
    ('shipped',    'ارسال شد',        'fa-truck-fast'),
]


def order_track_view(request):
    """Guest order tracking: match on order_number + phone, no login."""
    order = None
    steps = None
    not_found = False
    submitted = False
    order_number = ''
    phone = ''

    if request.method == 'POST':
        submitted = True
        order_number = (request.POST.get('order_number') or '').strip()
        phone = (request.POST.get('phone') or '').strip()

        order = (Order.objects
                 .filter(order_number__iexact=order_number, phone=phone)
                 .prefetch_related('items')
                 .first())

        if order is None:
            not_found = True
        else:
            # Build the stepped progress state for the template.
            if order.status == 'cancelled':
                current = -1
            else:
                keys = [s[0] for s in TRACK_STEPS]
                current = keys.index(order.status) if order.status in keys else 0
            steps = [
                {
                    'label': label,
                    'icon': icon,
                    'done': (idx < current) or (idx == current and order.status != 'cancelled'),
                    'active': idx == current,
                }
                for idx, (key, label, icon) in enumerate(TRACK_STEPS)
            ]

    return render(request, 'orders/track.html', {
        'order': order,
        'steps': steps,
        'not_found': not_found,
        'submitted': submitted,
        'order_number': order_number,
        'phone': phone,
    })
