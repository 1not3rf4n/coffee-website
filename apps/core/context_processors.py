from apps.core.models import SiteSettings
from apps.reservations.models import ReservationSettings
from apps.cart.cart import Cart

def site_context(request):
    settings, _ = SiteSettings.objects.get_or_create(id=1)
    res_settings, _ = ReservationSettings.objects.get_or_create(id=1)
    cart = Cart(request)
    
    return {
        'site_settings': settings,
        'reservation_settings': res_settings,
        'cart_total_items': len(cart),
        'cart_total_price': cart.get_total_price(),
    }
