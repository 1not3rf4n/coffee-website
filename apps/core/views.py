from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, time
import random

from apps.core.models import SiteSettings, LuckyWheelCoupon
from apps.menu.models import MenuCategory, MenuItem
from apps.shop.models import Product

def get_live_status(site_settings):
    try:
        now = datetime.now().time()
        open_h, open_m = map(int, site_settings.open_time.split(':'))
        close_h, close_m = map(int, site_settings.close_time.split(':'))
        
        open_t = time(open_h, open_m)
        close_t = time(close_h, close_m)
        
        is_open = open_t <= now <= close_t
        return {
            'is_open': is_open,
            'status_text': 'هم‌اکنون باز است (در حال پذیرش مشتریان)' if is_open else 'هم‌اکنون بسته است',
            'open_time': site_settings.open_time,
            'close_time': site_settings.close_time
        }
    except Exception:
        return {'is_open': True, 'status_text': 'هم‌اکنون باز است', 'open_time': '08:00', 'close_time': '23:00'}

def landing_view(request):
    site_settings, _ = SiteSettings.objects.get_or_create(id=1)
    categories = MenuCategory.objects.filter(is_active=True).prefetch_related('items')
    featured_menu_items = MenuItem.objects.filter(is_active=True, is_featured=True)[:6]
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:4]
    
    live_status = get_live_status(site_settings)
    coupons = LuckyWheelCoupon.objects.filter(is_active=True)

    context = {
        'site_settings': site_settings,
        'categories': categories,
        'featured_menu_items': featured_menu_items,
        'featured_products': featured_products,
        'live_status': live_status,
        'coupons': coupons
    }
    return render(request, 'landing.html', context)

def spin_wheel_api(request):
    coupons = list(LuckyWheelCoupon.objects.filter(is_active=True))
    if not coupons:
        return JsonResponse({
            'success': True,
            'title': '۱۰٪ تخفیف اختصاصی باریستا',
            'code': 'COFFEE10',
            'discount': 10
        })
    winning_coupon = random.choice(coupons)
    return JsonResponse({
        'success': True,
        'title': winning_coupon.title,
        'code': winning_coupon.code,
        'discount': winning_coupon.discount_percent
    })

def quiz_recommend_api(request):
    mood = request.GET.get('mood', 'energetic')
    flavor = request.GET.get('flavor', 'bitter')
    
    if flavor == 'sweet':
        item = MenuItem.objects.filter(is_active=True, title__icontains='کارامل').first() or \
               MenuItem.objects.filter(is_active=True, title__icontains='موکا').first()
        rec_title = item.title if item else "کاپوچینو با کارامل برشته"
        rec_desc = "ترکیبی مخملی از اسپرسو، شیر تازه و سس کارامل اختصاصی کافه."
    elif flavor == 'fruity':
        item = MenuItem.objects.filter(is_active=True, temperature='cold').first()
        rec_title = item.title if item else "آیس آمریکانو با عصاره مرکبات"
        rec_desc = "قهوه 100% عربیکا با نت‌های مرکباتی روشن و شاداب‌کننده."
    else:
        item = MenuItem.objects.filter(is_active=True, title__icontains='اسپرسو').first()
        rec_title = item.title if item else "دوبل اسپرسو رست تیره (Dark Roast)"
        rec_desc = "طعم اصیل و پرکافئین قهوه با کرمای غلیظ طلایی."

    return JsonResponse({
        'success': True,
        'title': rec_title,
        'desc': rec_desc,
        'price': getattr(item, 'final_price', 65000) if item else 65000
    })
