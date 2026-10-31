from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from apps.core.models import SiteSettings, LuckyWheelCoupon
from apps.menu.models import MenuCategory, MenuItem
from apps.reservations.models import TableReservation, ReservationSettings
from apps.shop.models import Product, ProductCategory
from apps.orders.models import Order

@staff_member_required
def dashboard_index_view(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    paid_orders = Order.objects.filter(status='paid').count()
    
    total_reservations = TableReservation.objects.count()
    pending_reservations = TableReservation.objects.filter(status='pending').count()
    
    total_menu_items = MenuItem.objects.count()
    active_menu_items = MenuItem.objects.filter(is_active=True).count()

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'paid_orders': paid_orders,
        'total_reservations': total_reservations,
        'pending_reservations': pending_reservations,
        'total_menu_items': total_menu_items,
        'active_menu_items': active_menu_items,
    }
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def dashboard_settings_view(request):
    site_settings, _ = SiteSettings.objects.get_or_create(id=1)
    res_settings, _ = ReservationSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        site_settings.site_name = request.POST.get('site_name', site_settings.site_name)
        site_settings.tagline = request.POST.get('tagline', site_settings.tagline)
        site_settings.primary_color = request.POST.get('primary_color', site_settings.primary_color)
        site_settings.secondary_color = request.POST.get('secondary_color', site_settings.secondary_color)
        
        site_settings.is_hero_animation_active = request.POST.get('is_hero_animation_active') == 'on'
        site_settings.is_menu_active = request.POST.get('is_menu_active') == 'on'
        site_settings.is_shop_active = request.POST.get('is_shop_active') == 'on'
        site_settings.is_reservation_active = request.POST.get('is_reservation_active') == 'on'
        site_settings.is_order_tracking_active = request.POST.get('is_order_tracking_active') == 'on'
        site_settings.is_quiz_active = request.POST.get('is_quiz_active') == 'on'
        site_settings.is_lucky_wheel_active = request.POST.get('is_lucky_wheel_active') == 'on'
        site_settings.is_soundscape_active = request.POST.get('is_soundscape_active') == 'on'
        
        site_settings.open_time = request.POST.get('open_time', site_settings.open_time)
        site_settings.close_time = request.POST.get('close_time', site_settings.close_time)
        site_settings.phone = request.POST.get('phone', site_settings.phone)
        site_settings.address = request.POST.get('address', site_settings.address)
        site_settings.save()

        # Reservation settings
        res_settings.require_deposit = request.POST.get('require_deposit') == 'on'
        res_settings.deposit_amount = int(request.POST.get('deposit_amount', res_settings.deposit_amount or 0))
        res_settings.save()

        messages.success(request, "تنظیمات دیزاین، پوسته و رزرو سایت با موفقیت بروزرسانی شد.")
        return redirect('dashboard:settings')

    return render(request, 'dashboard/settings.html', {
        'site_settings': site_settings,
        'res_settings': res_settings
    })

@staff_member_required
def dashboard_menu_view(request):
    categories = MenuCategory.objects.all().order_by('display_order')
    items = MenuItem.objects.all().select_related('category').order_by('display_order')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'toggle_item':
            item_id = request.POST.get('item_id')
            item = get_object_or_404(MenuItem, id=item_id)
            item.is_active = not item.is_active
            item.save()
            messages.success(request, f"وضعیت {item.title} به {'روشن / موجود' if item.is_active else 'خاموش / ناموجود'} تغییر کرد.")
            
        elif action == 'toggle_category':
            cat_id = request.POST.get('cat_id')
            cat = get_object_or_404(MenuCategory, id=cat_id)
            cat.is_active = not cat.is_active
            cat.save()
            messages.success(request, f"وضعیت دسته‌بندی {cat.title} بروزرسانی شد.")

        elif action == 'quick_edit_item':
            item_id = request.POST.get('item_id')
            item = get_object_or_404(MenuItem, id=item_id)
            item.price = int(request.POST.get('price', item.price))
            item.discount_price = int(request.POST.get('discount_price', item.discount_price))
            item.display_order = int(request.POST.get('display_order', item.display_order))
            item.save()
            messages.success(request, f"قیمت و چیدمان {item.title} ویرایش شد.")

        elif action == 'add_item':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(MenuCategory, id=category_id)
            MenuItem.objects.create(
                category=category,
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                price=int(request.POST.get('price', 50000)),
                discount_price=int(request.POST.get('discount_price', 0)),
                badge_text=request.POST.get('badge_text', ''),
                temperature=request.POST.get('temperature', 'hot'),
                is_active=True
            )
            messages.success(request, "آیتم جدید با موفقیت به منو اضافه شد.")

        return redirect('dashboard:menu')

    return render(request, 'dashboard/menu.html', {'categories': categories, 'items': items})

@staff_member_required
def dashboard_reservations_view(request):
    reservations = TableReservation.objects.all()
    if request.method == 'POST':
        res_id = request.POST.get('reservation_id')
        new_status = request.POST.get('status')
        res = get_object_or_404(TableReservation, id=res_id)
        res.status = new_status
        res.save()
        messages.success(request, f"وضعیت رزرو {res.full_name} به {res.get_status_display()} تغییر یافت.")
        return redirect('dashboard:reservations')

    return render(request, 'dashboard/reservations.html', {'reservations': reservations})

@staff_member_required
def dashboard_orders_view(request):
    orders = Order.objects.all().prefetch_related('items')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        messages.success(request, f"وضعیت سفارش {order.order_number} تغییر یافت.")
        return redirect('dashboard:orders')

    return render(request, 'dashboard/orders.html', {'orders': orders})
