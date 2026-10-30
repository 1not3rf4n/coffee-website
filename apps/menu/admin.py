from django.contrib import admin
from django.utils.html import format_html
from .models import MenuCategory, MenuItem


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'item_count', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        from django.db.models import Count
        return super().get_queryset(request).annotate(_ic=Count('items'))

    @admin.display(description='تعداد آیتم', ordering='_ic')
    def item_count(self, obj):
        return obj._ic


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'thumb', 'title', 'category', 'price_display',
        'temperature', 'is_active', 'is_featured', 'display_order',
    )
    list_display_links = ('thumb', 'title')
    list_editable = ('is_active', 'is_featured', 'display_order')
    list_filter = ('category', 'is_active', 'is_featured', 'temperature')
    search_fields = ('title', 'description')
    list_select_related = ('category',)
    list_per_page = 40
    actions = ('activate', 'deactivate')

    @admin.display(description='')
    def thumb(self, obj):
        return format_html(
            '<img src="{}" style="width:44px; height:44px; object-fit:cover; '
            'border-radius:8px; border:1px solid #444;">', obj.get_image_url,
        )

    @admin.display(description='قیمت', ordering='price')
    def price_display(self, obj):
        if obj.discount_percent:
            return format_html(
                '<span style="text-decoration:line-through; color:#999;">{}</span>'
                '&nbsp;<span style="color:#66bb6a; font-weight:700;">{} ت</span>',
                f"{obj.price:,}", f"{obj.final_price:,}",
            )
        return format_html('<span style="font-weight:700;">{} ت</span>', f"{obj.price:,}")

    @admin.action(description='روشن کردن آیتم‌های انتخابی')
    def activate(self, request, queryset):
        n = queryset.update(is_active=True)
        self.message_user(request, f"{n} آیتم روشن شد.")

    @admin.action(description='خاموش کردن آیتم‌های انتخابی')
    def deactivate(self, request, queryset):
        n = queryset.update(is_active=False)
        self.message_user(request, f"{n} آیتم خاموش شد.")
