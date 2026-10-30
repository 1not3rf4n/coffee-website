from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, LuckyWheelCoupon


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone', 'theme_swatch',
                    'is_hero_animation_active', 'is_menu_active',
                    'is_shop_active', 'is_reservation_active')

    fieldsets = (
        ('برندینگ', {
            'fields': ('site_name', 'tagline', 'logo_text', 'logo_image'),
        }),
        ('رنگ‌بندی پوسته', {
            'fields': ('primary_color', 'secondary_color', 'accent_glow'),
        }),
        ('بخش‌های فعال سایت', {
            'fields': ('is_hero_animation_active', 'is_menu_active',
                       'is_shop_active', 'is_reservation_active',
                       'is_quiz_active', 'is_lucky_wheel_active',
                       'is_soundscape_active'),
        }),
        ('ساعت کاری و تماس', {
            'fields': ('open_time', 'close_time', 'address', 'phone', 'instagram'),
        }),
    )

    @admin.display(description='رنگ پوسته')
    def theme_swatch(self, obj):
        return format_html(
            '<span style="display:inline-block; width:18px; height:18px; '
            'border-radius:50%; background:{}; border:1px solid #000; '
            'vertical-align:middle;"></span> '
            '<span style="display:inline-block; width:18px; height:18px; '
            'border-radius:50%; background:{}; border:1px solid #000; '
            'vertical-align:middle;"></span>',
            obj.primary_color, obj.accent_glow,
        )

    # Singleton: block adding a second settings row.
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(LuckyWheelCoupon)
class LuckyWheelCouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'discount_percent', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('code', 'title')
