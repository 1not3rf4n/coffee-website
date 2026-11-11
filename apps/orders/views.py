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
            status='pending',
            payment_method='card_to_card'
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

    if request.method == 'POST':
        if 'receipt_image' in request.FILES:
            order.receipt_image = request.FILES['receipt_image']
        
        order.card_last_digits = request.POST.get('card_last_digits', '').strip()
        user_tracking = request.POST.get('tracking_code', '').strip()
        if user_tracking:
            order.tracking_code = user_tracking
        else:
            order.tracking_code = f"REC-{random.randint(100000, 999999)}"

        order.status = 'awaiting_approval'
        order.payment_method = 'card_to_card'
        order.save()

        # کاهش موجودی انبار پس از ارسال فیش
        for item in order.items.all():
            if item.product:
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()

        messages.success(request, "فیش واریزی با موفقیت دریافت شد و در دست بررسی تیم کافه قرار گرفت.")
        return redirect('orders:order_success', order_id=order.id)

    return render(request, 'orders/payment_mock.html', {'order': order})

def payment_verify_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    action = request.GET.get('action', 'success')

    if action == 'success':
        order.status = 'paid'
        if not order.tracking_code:
            order.tracking_code = f"TRK-{random.randint(100000, 999999)}"
        order.save()
        for item in order.items.all():
            if item.product:
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()
        messages.success(request, "پرداخت با موفقیت تأیید شد!")
        return redirect('orders:order_success', order_id=order.id)
    else:
        order.status = 'cancelled'
        order.save()
        messages.error(request, "پرداخت توسط کاربر لغو گردید.")
        return render(request, 'orders/payment_failed.html', {'order': order})

def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


# مراحل لایو پیگیری وضعیت سفارش
TRACK_STEPS = [
    ('pending',           'ثبت سفارش',                'fa-file-invoice'),
    ('awaiting_approval', 'بررسی فیش واریز',          'fa-clock'),
    ('paid',              'تأیید پرداخت',              'fa-credit-card'),
    ('processing',        'آماده‌سازی و برشته‌کاری',  'fa-fire'),
    ('shipped',           'تحویل پیک / ارسال',         'fa-truck-fast'),
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

        if order_number and phone:
            order = Order.objects.filter(
                order_number__iexact=order_number,
                phone__endswith=phone[-10:],
            ).prefetch_related('items').first()

            if not order:
                not_found = True
            else:
                steps = _build_track_steps(order.status)
        else:
            not_found = True

    return render(request, 'orders/track.html', {
        'order': order,
        'steps': steps,
        'not_found': not_found,
        'submitted': submitted,
        'order_number': order_number,
        'phone': phone,
    })


def _build_track_steps(current_status):
    order_pipeline = ['pending', 'awaiting_approval', 'paid', 'processing', 'shipped']
    if current_status not in order_pipeline:
        return [
            {'code': s[0], 'label': s[1], 'icon': s[2], 'state': 'done' if s[0] == 'pending' else 'cancelled'}
            for s in TRACK_STEPS
        ]

    current_idx = order_pipeline.index(current_status)
    out = []
    for idx, (code, label, icon) in enumerate(TRACK_STEPS):
        if idx < current_idx:
            state = 'done'
        elif idx == current_idx:
            state = 'current'
        else:
            state = 'upcoming'
        out.append({'code': code, 'label': label, 'icon': icon, 'state': state})
    return out
