from django.contrib import admin
from django.utils.html import format_html
from .models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_count', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        from django.db.models import Count
        return super().get_queryset(request).annotate(_pc=Count('products'))

    @admin.display(description='تعداد محصول', ordering='_pc')
    def product_count(self, obj):
        return obj._pc


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'thumb', 'title', 'category', 'price_display',
        'discount_badge', 'stock_badge', 'roast_level',
        'is_active', 'is_featured',
    )
    list_display_links = ('thumb', 'title')
    list_editable = ('is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured', 'roast_level')
    search_fields = ('title', 'description', 'flavor_notes')
    prepopulated_fields = {'slug': ('title',)}
    list_select_related = ('category',)
    list_per_page = 30
    readonly_fields = ('preview',)
    actions = ('activate', 'deactivate', 'feature', 'unfeature')

    fieldsets = (
        ('مشخصات محصول', {
            'fields': ('title', 'slug', 'category', 'description', 'flavor_notes'),
        }),
        ('قیمت و موجودی', {
            'fields': ('price', 'discount_price', 'stock'),
        }),
        ('پروفایل قهوه', {
            'fields': ('roast_level', 'acidity_level', 'bitterness_level'),
        }),
        ('تصویر', {
            'fields': ('image', 'image_url', 'preview'),
        }),
        ('نمایش', {
            'fields': ('is_active', 'is_featured'),
        }),
    )

    @admin.display(description='')
    def thumb(self, obj):
        url = obj.get_image_url
        return format_html(
            '<img src="{}" style="width:46px; height:46px; object-fit:cover; '
            'border-radius:8px; border:1px solid #444;">', url,
        )

    @admin.display(description='پیش‌نمایش')
    def preview(self, obj):
        url = obj.get_image_url
        return format_html(
            '<img src="{}" style="max-width:220px; border-radius:12px; '
            'border:1px solid #444;">', url,
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

    @admin.display(description='تخفیف')
    def discount_badge(self, obj):
        pct = obj.discount_percent
        if pct:
            return format_html(
                '<span style="background:#C62828; color:#fff; padding:2px 8px; '
                'border-radius:12px; font-size:0.75rem; font-weight:700;">{}%-</span>', pct,
            )
        return "—"

    @admin.display(description='موجودی', ordering='stock')
    def stock_badge(self, obj):
        if obj.stock <= 0:
            bg, txt = '#C62828', 'ناموجود'
        elif obj.stock <= 5:
            bg, txt = '#E65100', f'کم ({obj.stock})'
        else:
            bg, txt = '#2E7D32', str(obj.stock)
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 10px; '
            'border-radius:12px; font-size:0.78rem; font-weight:700;">{}</span>', bg, txt,
        )

    @admin.action(description='فعال کردن محصولات انتخابی')
    def activate(self, request, queryset):
        n = queryset.update(is_active=True)
        self.message_user(request, f"{n} محصول فعال شد.")

    @admin.action(description='غیرفعال کردن محصولات انتخابی')
    def deactivate(self, request, queryset):
        n = queryset.update(is_active=False)
        self.message_user(request, f"{n} محصول غیرفعال شد.")

    @admin.action(description='افزودن به محصولات ویژه')
    def feature(self, request, queryset):
        n = queryset.update(is_featured=True)
        self.message_user(request, f"{n} محصول ویژه شد.")

    @admin.action(description='حذف از محصولات ویژه')
    def unfeature(self, request, queryset):
        n = queryset.update(is_featured=False)
        self.message_user(request, f"{n} محصول از حالت ویژه خارج شد.")
