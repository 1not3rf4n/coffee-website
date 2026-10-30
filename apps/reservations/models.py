from django.db import models

class TableReservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار تایید'),
        ('confirmed', 'تایید شده'),
        ('cancelled', 'لغو شده'),
    )

    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    date = models.DateField(verbose_name="تاریخ رزرو")
    time = models.TimeField(verbose_name="ساعت رزرو")
    guests_count = models.IntegerField(default=2, verbose_name="تعداد نفرات")
    table_number = models.IntegerField(blank=True, null=True, verbose_name="شماره میز (اختیاری)")
    special_request = models.TextField(blank=True, verbose_name="توضیحات یا درخواست ویژه")
    
    require_deposit = models.BooleanField(default=False, verbose_name="نیاز به پرداحت بیعانه داشته")
    deposit_paid = models.BooleanField(default=False, verbose_name="بیعانه پرداخت شده")
    deposit_amount = models.IntegerField(default=0, verbose_name="مبلغ بیعانه (تومان)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "رزرو میز"
        verbose_name_plural = "رزروهای میز"

    def __str__(self):
        return f"رزرو {self.full_name} برای {self.guests_count} نفر در تاریخ {self.date}"

class ReservationSettings(models.Model):
    is_enabled = models.BooleanField(default=True, verbose_name="امکان رزرو آنلاین فعال باشد")
    require_deposit = models.BooleanField(default=False, verbose_name="نیاز به پرداخت بیعانه باشد (دست ادمین)")
    deposit_amount = models.IntegerField(default=50000, verbose_name="مبلغ بیعانه هر رزرو (تومان)")
    max_guests = models.IntegerField(default=10, verbose_name="حداکثر تعداد نفرات در یک میز")

    class Meta:
        verbose_name = "تنظیمات رزرو میز"
        verbose_name_plural = "تنظیمات عمومی رزرو"

    def __str__(self):
        return f"تنظیمات رزرو (بیعانه: {'اجباری' if self.require_deposit else 'رایگان'})"
