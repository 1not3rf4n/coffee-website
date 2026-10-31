from apps.core.models import SiteSettings
from apps.reservations.models import ReservationSettings
from apps.cart.cart import Cart
from apps.core.views import get_live_status

def site_context(request):
    try:
        settings, _ = SiteSettings.objects.get_or_create(id=1)
    except Exception as e:
        settings = None

    try:
        res_settings, _ = ReservationSettings.objects.get_or_create(id=1)
    except Exception as e:
        res_settings = None

    try:
        live_status = get_live_status(settings) if settings else {'is_open': True, 'status_text': 'هم‌اکنون باز است'}
    except Exception:
        live_status = {'is_open': True, 'status_text': 'هم‌اکنون باز است'}

    try:
        cart = Cart(request)
        cart_total_items = len(cart)
        cart_total_price = cart.get_total_price()
    except Exception as e:
        cart_total_items = 0
        cart_total_price = 0
    
    return {
        'site_settings': settings,
        'reservation_settings': res_settings,
        'live_status': live_status,
        'cart_total_items': cart_total_items,
        'cart_total_price': cart_total_price,
    }
