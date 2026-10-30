from apps.core.models import SiteSettings
from apps.reservations.models import ReservationSettings
from apps.cart.cart import Cart

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
        cart = Cart(request)
        cart_total_items = len(cart)
        cart_total_price = cart.get_total_price()
    except Exception as e:
        cart_total_items = 0
        cart_total_price = 0
    
    return {
        'site_settings': settings,
        'reservation_settings': res_settings,
        'cart_total_items': cart_total_items,
        'cart_total_price': cart_total_price,
    }
