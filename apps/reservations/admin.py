from django.contrib import admin
from django.utils.html import format_html
from .models import TableReservation, ReservationSettings


RES_STATUS_COLOURS = {
    'pending':   '#E65100',
    'confirmed': '#2E7D32',
    'cancelled': '#C62828',
}


@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'phone', 'date', 'time', 'guests_count',
        'table_number', 'deposit_state', 'status_badge',
    )
    list_filter = ('status', 'date', 'require_deposit', 'deposit_paid')
    search_fields = ('full_name', 'phone')
    date_hierarchy = 'date'
    ordering = ('-created_at',)
    list_per_page = 30
    actions = ('confirm', 'cancel', 'mark_deposit_paid')

    @admin.display(description='وضعیت', ordering='status')
    def status_badge(self, obj):
        bg = RES_STATUS_COLOURS.get(obj.status, '#555')
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 12px; '
            'border-radius:20px; font-size:0.8rem; font-weight:700;">{}</span>',
            bg, obj.get_status_display(),
        )

    @admin.display(description='بیعانه')
    def deposit_state(self, obj):
        if not obj.require_deposit:
            return format_html('<span style="color:#888;">آزاد</span>')
        if obj.deposit_paid:
            return format_html('<span style="color:#66bb6a; font-weight:700;">پرداخت شده</span>')
        return format_html('<span style="color:#ff9800; font-weight:700;">در انتظار</span>')

    @admin.action(description='تایید رزروهای انتخابی')
    def confirm(self, request, queryset):
        n = queryset.update(status='confirmed')
        self.message_user(request, f"{n} رزرو تایید شد.")

    @admin.action(description='لغو رزروهای انتخابی')
    def cancel(self, request, queryset):
        n = queryset.update(status='cancelled')
        self.message_user(request, f"{n} رزرو لغو شد.")

    @admin.action(description='ثبت پرداخت بیعانه')
    def mark_deposit_paid(self, request, queryset):
        n = queryset.update(deposit_paid=True)
        self.message_user(request, f"بیعانه {n} رزرو پرداخت‌شده ثبت شد.")


@admin.register(ReservationSettings)
class ReservationSettingsAdmin(admin.ModelAdmin):
    list_display = ('is_enabled', 'require_deposit', 'deposit_amount', 'max_guests')
