from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.reservations.models import TableReservation, ReservationSettings

def reservation_view(request):
    res_settings, _ = ReservationSettings.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests_count = request.POST.get('guests_count', 2)
        table_number = request.POST.get('table_number') or None
        special_request = request.POST.get('special_request', '')
        
        reservation = TableReservation.objects.create(
            full_name=full_name,
            phone=phone,
            date=date,
            time=time,
            guests_count=guests_count,
            table_number=table_number,
            special_request=special_request,
            require_deposit=res_settings.require_deposit,
            deposit_amount=res_settings.deposit_amount if res_settings.require_deposit else 0,
            status='pending'
        )

        if res_settings.require_deposit:
            return redirect('reservations:deposit_pay', reservation_id=reservation.id)

        messages.success(request, f"رزرو میز شما با موفقیت برای {full_name} ثبت شد! به زودی جهت تایید نهایی تماس گرفته خواهد شد.")
        return redirect('reservations:success', reservation_id=reservation.id)

    return render(request, 'reservations.html', {'res_settings': res_settings})

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
