import json
from apps.core.models import SiteSettings, CafeMusic
from apps.reservations.models import ReservationSettings
from apps.cart.cart import Cart
from apps.core.views import get_live_status

def site_context(request):
    try:
        settings, _ = SiteSettings.objects.get_or_create(id=1)
    except Exception:
        settings = None

    try:
        res_settings, _ = ReservationSettings.objects.get_or_create(id=1)
    except Exception:
        res_settings = None

    try:
        live_status = get_live_status(settings) if settings else {'is_open': True, 'status_text': 'هم‌اکنون باز است'}
    except Exception:
        live_status = {'is_open': True, 'status_text': 'هم‌اکنون باز است'}

    try:
        cart = Cart(request)
        cart_total_items = len(cart)
        cart_total_price = cart.get_total_price()
    except Exception:
        cart_total_items = 0
        cart_total_price = 0

    # بارگذاری پلی‌لیست موزیک‌های فعال کافه
    playlist_items = []
    try:
        active_musics = CafeMusic.objects.filter(is_active=True).order_by('order', '-created_at')
        for m in active_musics:
            if m.audio_file:
                playlist_items.append({
                    'id': m.id,
                    'title': m.title,
                    'artist': m.artist or 'کافه عرفان',
                    'url': m.audio_file.url,
                })
    except Exception:
        pass

    # در صورتی که ادمین هنوز فایلی آپلود نکرده باشد، یک ترک پیش‌فرض ملایم کافه قرار می‌دهیم
    if not playlist_items:
        playlist_items = [
            {
                'id': 0,
                'title': 'صدای آرامش‌بخش کافه',
                'artist': 'نوین کافه',
                'url': 'https://assets.mixkit.co/music/preview/mixkit-chill-bro-494.mp3',
            }
        ]

    return {
        'site_settings': settings,
        'reservation_settings': res_settings,
        'live_status': live_status,
        'cart_total_items': cart_total_items,
        'cart_total_price': cart_total_price,
        'cafe_playlist_json': json.dumps(playlist_items, ensure_ascii=False),
        'cafe_playlist': playlist_items,
    }
