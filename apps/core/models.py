from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="کافه اسپرسو نوین")
    tagline = models.CharField(max_length=200, default="عطر اصیل دانه برشته قهوه")
    logo_text = models.CharField(max_length=50, default="NOVIN CAFE")
    logo_image = models.ImageField(upload_to='site/', blank=True, null=True)
    
    primary_color = models.CharField(max_length=10, default="#E65100", help_text="کد رنگ نارنجی اصلی")
    secondary_color = models.CharField(max_length=10, default="#121417", help_text="کد رنگ طوسی و زغالی")
    accent_glow = models.CharField(max_length=10, default="#FF9800", help_text="رنگ درخشش")
    
    is_hero_animation_active = models.BooleanField(default=True, verbose_name="فعال بودن انیمیشن لندینگ قهوه")
    is_menu_active = models.BooleanField(default=True, verbose_name="فعال بودن منوی حضوری")
    is_shop_active = models.BooleanField(default=True, verbose_name="فعال بودن فروشگاه آنلاین")
    is_reservation_active = models.BooleanField(default=True, verbose_name="فعال بودن رزرو میز")
    is_order_tracking_active = models.BooleanField(default=True, verbose_name="فعال بودن پیگیری سفارش")
    is_quiz_active = models.BooleanField(default=True, verbose_name="فعال بودن تست هوشمند قهوه")
    is_lucky_wheel_active = models.BooleanField(default=True, verbose_name="فعال بودن گردونه شانس")
    is_soundscape_active = models.BooleanField(default=True, verbose_name="فعال بودن پلیر صدای کافه")
    
    open_time = models.CharField(max_length=10, default="08:00", verbose_name="ساعت شروع کار")
    close_time = models.CharField(max_length=10, default="23:00", verbose_name="ساعت پایان کار")
    address = models.TextField(default="تهران، خیابان ولیعصر، بالاتر از پارک ساعی، پلاک ۱۲۰", verbose_name="آدرس کافه")
    phone = models.CharField(max_length=20, default="021-88889900", verbose_name="تلفن تماس")
    instagram = models.CharField(max_length=100, default="@novin_coffee", verbose_name="اینستاگرام")

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات عمومی سایت"

    def __str__(self):
        return self.site_name

class LuckyWheelCoupon(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name="کد تخفیف")
    title = models.CharField(max_length=100, verbose_name="عنوان جایزه")
    discount_percent = models.IntegerField(default=10, verbose_name="درصد تخفیف")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "کپون گردونه شانس"
        verbose_name_plural = "کپون‌های گردونه شانس"

    def __str__(self):
        return f"{self.title} ({self.discount_percent}%)"
