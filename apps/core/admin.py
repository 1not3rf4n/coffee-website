from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, CafeMusic, LuckyWheelCoupon


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'site_name', 'phone', 'instagram', 'bank_name', 'card_holder',
        'is_soundscape_active', 'soundscape_autoplay', 'is_card_to_card_active',
        'theme_swatch',
    )

    fieldsets = (
        ('برندینگ و اطلاعات عمومی', {
            'fields': ('site_name', 'tagline', 'logo_text', 'logo_image'),
        }),
        ('رنگ‌بندی اختصاصی پوسته', {
            'fields': ('primary_color', 'secondary_color', 'accent_glow'),
        }),
        ('درگاه پرداخت کارت به کارت', {
            'description': 'مشخصات کارت بانکی که در مرحله تسویه‌حساب به مشتری نمایش داده می‌شود.',
            'fields': ('is_card_to_card_active', 'bank_name', 'card_number', 'card_holder', 'shaba_number'),
        }),
        ('موزیک و صدای زنده کافه', {
            'description': 'پخش موزیک پس‌زمینه در کل صفحات سایت',
            'fields': ('is_soundscape_active', 'soundscape_autoplay'),
        }),
        ('لوکیشن، نقشه و مسیریابی', {
            'description': 'آدرس و لینک مستقیم هدایت به اپ‌های مسیریابی مثل نشان و گوگل‌مپ',
            'fields': ('address', 'neshan_url', 'google_maps_url', 'map_image', 'map_iframe'),
        }),
        ('راه‌های تماس و شبکه‌های اجتماعی', {
            'fields': ('phone', 'instagram', 'open_time', 'close_time'),
        }),
        ('وضعیت بخش‌های فعال سایت', {
            'fields': (
                'is_hero_animation_active', 'is_menu_active',
                'is_shop_active', 'is_reservation_active',
                'is_order_tracking_active', 'is_quiz_active',
                'is_lucky_wheel_active',
            ),
        }),
    )

    @admin.display(description='رنگ پوسته')
    def theme_swatch(self, obj):
        return format_html(
            '<span style="display:inline-block; width:18px; height:18px; '
            'border-radius:50%; background:{}; border:1px solid #333; '
            'vertical-align:middle; box-shadow:0 0 6px {};"></span> '
            '<span style="display:inline-block; width:18px; height:18px; '
            'border-radius:50%; background:{}; border:1px solid #333; '
            'vertical-align:middle;"></span>',
            obj.primary_color, obj.primary_color, obj.secondary_color,
        )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(CafeMusic)
class CafeMusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'order', 'is_active', 'audio_preview', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'artist')

    @admin.display(description='پیش‌شنوایی موزیک')
    def audio_preview(self, obj):
        if obj.audio_file:
            return format_html(
                '<audio controls preload="none" style="height:30px; width:220px;">'
                '<source src="{}" type="audio/mpeg">'
                'مرورگر شما از پخش صدا پشتیبانی نمی‌کند.'
                '</audio>',
                obj.audio_file.url,
            )
        return "بدون فایل"


@admin.register(LuckyWheelCoupon)
class LuckyWheelCouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'discount_percent', 'is_active')
    list_editable = ('discount_percent', 'is_active')
    search_fields = ('code', 'title')
