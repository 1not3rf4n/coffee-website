from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


STATUS_COLOURS = {
    'pending':           ('#9E9E9E', '#fff'),   # خاکستری
    'awaiting_approval': ('#F57C00', '#fff'),   # نارنجی پررنگ / چشمک‌زن
    'paid':              ('#2E7D32', '#fff'),   # سبز
    'processing':        ('#0288D1', '#fff'),   # آبی
    'shipped':           ('#7B1FA2', '#fff'),   # بنفش
    'cancelled':         ('#C62828', '#fff'),   # قرمز
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
            return f"{obj.total_item_price:,} تومان"
        return "—"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'full_name', 'phone',
        'total_price_display', 'status_badge', 'payment_method_display',
        'receipt_preview', 'items_count', 'created_at',
    )
    list_display_links = ('order_number', 'full_name')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'full_name', 'phone', 'tracking_code', 'card_last_digits')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'receipt_full_view', 'items_summary')
    list_per_page = 25
    actions = ('mark_approved_paid', 'mark_processing', 'mark_shipped', 'mark_cancelled')

    fieldsets = (
        ('اطلاعات سفارش و وضعیت', {
            'fields': ('order_number', 'status', 'created_at'),
        }),
        ('اطلاعات خریدار', {
            'fields': ('full_name', 'phone', 'address'),
        }),
        ('اطلاعات پرداخت و فیش کارت به کارت', {
            'fields': (
                'total_price', 'payment_method', 'payment_gateway',
                'tracking_code', 'card_last_digits', 'receipt_image',
                'receipt_full_view', 'admin_note',
            ),
        }),
        ('خلاصه اقلام فاکتور', {
            'fields': ('items_summary',),
        }),
    )

    @admin.display(description='مبلغ کل')
    def total_price_display(self, obj):
        return f"{obj.total_price:,} تومان"

    @admin.display(description='روش پرداخت')
    def payment_method_display(self, obj):
        if obj.payment_method == 'card_to_card':
            return format_html('<span style="color:#F0782E; font-weight:700;"><i class="fa fa-credit-card"></i> کارت به کارت</span>')
        return "درگاه آنلاین"

    @admin.display(description='وضعیت')
    def status_badge(self, obj):
        bg, fg = STATUS_COLOURS.get(obj.status, ('#757575', '#fff'))
        label = obj.get_status_display()
        return format_html(
            '<span style="background:{}; color:{}; padding:4px 10px; border-radius:12px; '
            'font-size:11px; font-weight:700; white-space:nowrap; display:inline-block;">{}</span>',
            bg, fg, label,
        )

    @admin.display(description='فیش واریز')
    def receipt_preview(self, obj):
        if obj.receipt_image:
            return format_html(
                '<a href="{}" target="_blank" title="مشاهده فیش در اندازه بزرگ">'
                '<img src="{}" style="width:40px; height:40px; object-fit:cover; border-radius:6px; border:1px solid #E65100;" />'
                '</a>',
                obj.receipt_image.url, obj.receipt_image.url
            )
        return format_html('<span style="color:#888; font-size:11px;">بدون فیش</span>')

    @admin.display(description='پیش‌نمایش تصویر فیش واریز')
    def receipt_full_view(self, obj):
        if obj.receipt_image:
            return format_html(
                '<div style="margin:10px 0;">'
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-width:320px; max-height:350px; border-radius:10px; border:2px solid #F0782E; box-shadow:0 4px 15px rgba(0,0,0,0.5);" />'
                '</a>'
                '<p style="color:#aaa; font-size:12px; margin-top:6px;">(برای مشاهده در اندازه کامل روی تصویر کلیک کنید)</p>'
                '</div>',
                obj.receipt_image.url, obj.receipt_image.url
            )
        return "فیشی برای این سفارش آپلود نشده است."

    @admin.display(description='تعداد اقلام')
    def items_count(self, obj):
        return sum(item.quantity for item in obj.items.all())

    @admin.display(description='اقلام سفارش')
    def items_summary(self, obj):
        items = obj.items.all()
        if not items.exists():
            return "آیتمی ثبت نشده است."
        rows = "".join(
            f"<li><strong>{it.product_name}</strong> (نوع: {it.grind_type}) &times; {it.quantity} = {it.total_item_price:,} تومان</li>"
            for it in items
        )
        return format_html("<ul style='padding-right:18px;'>{}</ul>", format_html(rows))

    # اکشن‌های مدیریتی
    @admin.action(description='✓ تأیید فیش کارت‌به‌کارت و انتقال به آماده‌سازی')
    def mark_approved_paid(self, request, queryset):
        count = queryset.update(status='paid')
        self.message_user(request, f"{count} سفارش با موفقیت تأیید شد و به وضعیت «پرداخت شده / در حال آماده‌سازی» تغییر یافت.")

    @admin.action(description='🔄 تغییر به در حال پردازش و برشته‌کاری')
    def mark_processing(self, request, queryset):
        count = queryset.update(status='processing')
        self.message_user(request, f"{count} سفارش به وضعیت «در حال پردازش» تغییر یافت.")

    @admin.action(description='🚚 تغییر به تحویل پیک / ارسال شده')
    def mark_shipped(self, request, queryset):
        count = queryset.update(status='shipped')
        self.message_user(request, f"{count} سفارش به وضعیت «ارسال شده» تغییر یافت.")

    @admin.action(description='✗ رد فیش یا لغو سفارشات انتخابی')
    def mark_cancelled(self, request, queryset):
        count = queryset.update(status='cancelled')
        self.message_user(request, f"{count} سفارش لغو شد.")
