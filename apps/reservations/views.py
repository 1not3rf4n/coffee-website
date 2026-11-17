import datetime
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.reservations.models import TableReservation, ReservationSettings

def normalize_digits(s):
    if not s:
        return s
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    arabic_digits = '٠١٢٣٤٥٦٧٨٩'
    english_digits = '0123456789'
    res = str(s)
    for p, e in zip(persian_digits, english_digits):
        res = res.replace(p, e)
    for a, e in zip(arabic_digits, english_digits):
        res = res.replace(a, e)
    return res

def reservation_view(request):
    res_settings, _ = ReservationSettings.objects.get_or_create(id=1)
    today_str = datetime.date.today().isoformat()
    
    if request.method == 'POST':
        full_name = (request.POST.get('full_name') or '').strip()
        phone = normalize_digits(request.POST.get('phone') or '').strip()
        raw_date = normalize_digits(request.POST.get('date') or '').strip()
        raw_time = normalize_digits(request.POST.get('time') or '').strip()

        if not full_name or not phone or not raw_date or not raw_time:
            messages.error(request, "لطفاً تمامی فیلدهای الزامی (نام، تلفن، تاریخ و ساعت) را تکمیل فرمایید.")
            return render(request, 'reservations.html', {'res_settings': res_settings, 'today': today_str})

        # اعتبارسنجی و تبدیل تعداد نفرات
        try:
            guests_count = int(normalize_digits(request.POST.get('guests_count') or '2'))
            if guests_count < 1:
                guests_count = 1
        except (ValueError, TypeError):
            guests_count = 2

        # شماره میز اختیاری
        raw_table = normalize_digits(request.POST.get('table_number') or '').strip()
        table_number = int(raw_table) if raw_table.isdigit() else None
        special_request = (request.POST.get('special_request') or '').strip()

        try:
            reservation = TableReservation.objects.create(
                full_name=full_name,
                phone=phone,
                date=raw_date,
                time=raw_time,
                guests_count=guests_count,
                table_number=table_number,
                special_request=special_request,
                require_deposit=res_settings.require_deposit,
                deposit_amount=res_settings.deposit_amount if res_settings.require_deposit else 0,
                status='pending'
            )

            if res_settings.require_deposit and res_settings.deposit_amount > 0:
                return redirect('reservations:deposit_pay', reservation_id=reservation.id)

            messages.success(request, f"رزرو میز شما با موفقیت برای {full_name} ثبت شد! به زودی جهت هماهنگی نهایی با شما تماس گرفته خواهد شد.")
            return redirect('reservations:success', reservation_id=reservation.id)

        except Exception as err:
            messages.error(request, f"خطا در ثبت رزرو: لطفاً قالب تاریخ و ساعت انتخابی را مجدداً بررسی فرمایید.")
            return render(request, 'reservations.html', {'res_settings': res_settings, 'today': today_str})

    return render(request, 'reservations.html', {'res_settings': res_settings, 'today': today_str})

def deposit_pay_view(request, reservation_id):
    reservation = get_object_or_404(TableReservation, id=reservation_id)
    if request.method == 'POST':
        reservation.deposit_paid = True
        reservation.status = 'confirmed'
        reservation.save()
        messages.success(request, "بیعانه رزرو میز با موفقیت پرداخت و رزرو شما تایید شد!")
        return redirect('reservations:success', reservation_id=reservation.id)

    return render(request, 'reservations_deposit_pay.html', {'reservation': reservation})

def reservation_success_view(request, reservation_id):
    reservation = get_object_or_404(TableReservation, id=reservation_id)
    return render(request, 'reservations_success.html', {'reservation': reservation})
