from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


# Colour per order status, used for the pill badge in the list view.
STATUS_COLOURS = {
    'pending':    ('#9E9E9E', '#fff'),   # grey
    'paid':       ('#2E7D32', '#fff'),   # green
    'processing': ('#E65100', '#fff'),   # orange
    'shipped':    ('#1565C0', '#fff'),   # blue
    'cancelled':  ('#C62828', '#fff'),   # red
}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ('product',)
    readonly_fields = ('line_total',)
    fields = ('product', 'product_name', 'grind_type', 'price', 'quantity', 'line_total')

    @admin.display(description='جمع ردیف (تومان)')
    def line_total(self, obj):
        if obj.pk:
            return f"{obj.total_item_price:,}"
        return "—"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'full_name', 'phone',
        'total_price_display', 'status_badge', 'items_count',
        'payment_gateway', 'created_at',
    )
    list_display_links = ('order_number', 'full_name')
    list_filter = ('status', 'payment_gateway', 'created_at')
    search_fields = ('order_number', 'full_name', 'phone', 'tracking_code')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'items_summary')
    list_per_page = 30
    actions = ('mark_paid', 'mark_processing', 'mark_shipped', 'mark_cancelled')

    fieldsets = (
        ('اطلاعات سفارش', {
            'fields': ('order_number', 'status', 'created_at'),
        }),
        ('خریدار', {
            'fields': ('full_name', 'phone', 'address'),
        }),
        ('پرداخت و ارسال', {
            'fields': ('total_price', 'payment_gateway', 'tracking_code'),
        }),
        ('خلاصه اقلام', {
            'fields': ('items_summary',),
        }),
    )

    # ---- query optimisation: prefetch items so items_count/summary is cheap ----
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')

    @admin.display(description='مبلغ کل', ordering='total_price')
    def total_price_display(self, obj):
        return format_html('<span style="font-weight:700;">{} تومان</span>',
                           f"{obj.total_price:,}")

    @admin.display(description='وضعیت', ordering='status')
    def status_badge(self, obj):
        bg, fg = STATUS_COLOURS.get(obj.status, ('#555', '#fff'))
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 12px; '
            'border-radius:20px; font-size:0.8rem; font-weight:700; '
            'white-space:nowrap;">{}</span>',
            bg, fg, obj.get_status_display(),
        )

    @admin.display(description='تعداد اقلام')
    def items_count(self, obj):
        return obj.items.count()

    @admin.display(description='اقلام سفارش')
    def items_summary(self, obj):
        rows = obj.items.all()
        if not rows:
            return "—"
        html = '<table style="width:100%; border-collapse:collapse;">'
        html += ('<tr style="text-align:right; border-bottom:1px solid #ccc;">'
                 '<th>محصول</th><th>آسیاب</th><th>تعداد</th><th>قیمت واحد</th><th>جمع</th></tr>')
        for r in rows:
            html += format_html(
                '<tr style="border-bottom:1px solid #eee;">'
                '<td>{}</td><td>{}</td><td>{}</td><td>{} ت</td><td>{} ت</td></tr>',
                r.product_name, r.grind_type, r.quantity,
                f"{r.price:,}", f"{r.total_item_price:,}",
            )
        html += '</table>'
        return format_html(html)

    # ------------------------- bulk status actions -------------------------
    def _bulk_set(self, request, queryset, status, label):
        updated = queryset.update(status=status)
        self.message_user(request, f"{updated} سفارش به «{label}» تغییر یافت.")

    @admin.action(description='علامت‌گذاری به: پرداخت شده')
    def mark_paid(self, request, queryset):
        self._bulk_set(request, queryset, 'paid', 'پرداخت شده')

    @admin.action(description='علامت‌گذاری به: در حال برشته‌کاری')
    def mark_processing(self, request, queryset):
        self._bulk_set(request, queryset, 'processing', 'در حال پردازش')

    @admin.action(description='علامت‌گذاری به: ارسال شده')
    def mark_shipped(self, request, queryset):
        self._bulk_set(request, queryset, 'shipped', 'ارسال شده')

    @admin.action(description='علامت‌گذاری به: لغو شده')
    def mark_cancelled(self, request, queryset):
        self._bulk_set(request, queryset, 'cancelled', 'لغو شده')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'order', 'grind_type', 'price', 'quantity')
    search_fields = ('product_name', 'order__order_number')
    list_select_related = ('order', 'product')
    autocomplete_fields = ('product', 'order')
