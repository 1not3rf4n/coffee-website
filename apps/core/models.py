import re
from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="کافه اسپرسو نوین", verbose_name="نام کافه / برند")
    tagline = models.CharField(max_length=200, default="عطر اصیل دانه برشته قهوه", verbose_name="شعار کافه")
    logo_text = models.CharField(max_length=50, default="NOVIN CAFE", verbose_name="متن لوگو")
    logo_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="تصویر لوگوی کافه")
    
    # رنگ‌بندی
    primary_color = models.CharField(max_length=10, default="#F0782E", help_text="کد رنگ نارنجی اصلی (مثلاً #F0782E)", verbose_name="رنگ اصلی")
    secondary_color = models.CharField(max_length=10, default="#121417", help_text="کد رنگ پس‌زمینه زغالی و تیره", verbose_name="رنگ پس‌زمینه")
    accent_glow = models.CharField(max_length=10, default="#FF9354", help_text="رنگ درخشش نارنجی روشن", verbose_name="رنگ هایلایت")
    
    # ماژول‌های فعال
    is_hero_animation_active = models.BooleanField(default=True, verbose_name="فعال بودن انیمیشن لندینگ قهوه")
    is_menu_active = models.BooleanField(default=True, verbose_name="فعال بودن منوی حضوری")
    is_shop_active = models.BooleanField(default=True, verbose_name="فعال بودن فروشگاه آنلاین")
    is_reservation_active = models.BooleanField(default=True, verbose_name="فعال بودن رزرو میز")
    is_order_tracking_active = models.BooleanField(default=True, verbose_name="فعال بودن پیگیری سفارش")
    is_quiz_active = models.BooleanField(default=True, verbose_name="فعال بودن تست هوشمند قهوه")
    is_lucky_wheel_active = models.BooleanField(default=True, verbose_name="فعال بودن گردونه شانس")
    is_soundscape_active = models.BooleanField(default=True, verbose_name="فعال بودن پلیر موزیک کافه")
    soundscape_autoplay = models.BooleanField(default=True, verbose_name="پخش خودکار موزیک پس‌زمینه با ورود به سایت")
    
    # ساعت کاری، تماس و آدرس
    open_time = models.CharField(max_length=10, default="08:00", verbose_name="ساعت شروع کار")
    close_time = models.CharField(max_length=10, default="23:00", verbose_name="ساعت پایان کار")
    address = models.TextField(default="تهران، خیابان ولیعصر، بالاتر از پارک ساعی، پلاک ۱۲۰", verbose_name="آدرس دقیق کافه")
    phone = models.CharField(max_length=25, default="021-88889900", verbose_name="تلفن تماس مستقیم")
    instagram = models.CharField(max_length=100, default="@erfancafe", verbose_name="آیدی یا لینک پیج اینستاگرام")
    
    # لوکیشن و نشان
    neshan_url = models.URLField(max_length=300, blank=True, default="https://nshn.ir", verbose_name="لینک مستقیم مسیریابی در اپ نشان")
    google_maps_url = models.URLField(max_length=300, blank=True, default="https://maps.google.com", verbose_name="لینک مسیریابی در گوگل مپ")
    map_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="تصویر لوکیشن یا نقشه کافه")
    map_iframe = models.TextField(blank=True, default="", verbose_name="کد امبد آی‌فریم نقشه (اختیاری)")

    # پرداخت کارت به کارت
    is_card_to_card_active = models.BooleanField(default=True, verbose_name="فعال بودن درگاه پرداخت کارت به کارت")
    bank_name = models.CharField(max_length=50, default="بانک ملت", verbose_name="نام بانک صادرکننده کارت")
    card_number = models.CharField(max_length=30, default="6037-9975-1234-5678", verbose_name="شماره کارت ۱۶ رقمی")
    card_holder = models.CharField(max_length=100, default="عرفان رستمی", verbose_name="نام و نام خانوادگی صاحب حساب")
    shaba_number = models.CharField(max_length=35, blank=True, default="", verbose_name="شماره شبا (اختیاری)")

    class Meta:
        verbose_name = "تنظیمات عمومی سایت"
        verbose_name_plural = "تنظیمات عمومی سایت"

    def __str__(self):
        return self.site_name

    @property
    def clean_phone(self):
        """شماره تلفن تمیز جهت استفاده در تگ tel:"""
        if not self.phone:
            return ""
        return re.sub(r'[^\d+]', '', self.phone)

    @property
    def clean_instagram(self):
        """آیدی اینستاگرام بدون @ یا آدرس کامل"""
        if not self.instagram:
            return ""
        val = self.instagram.strip()
        if 'instagram.com/' in val:
            val = val.split('instagram.com/')[-1].split('/')[0].split('?')[0]
        return val.lstrip('@')

    @property
    def clean_card_number(self):
        """شماره کارت فقط اعداد جهت کپی آسان در کلیپ‌بورد"""
        if not self.card_number:
            return ""
        # تبدیل ارقام فارسی به انگلیسی در صورت وجود
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        res = self.card_number
        for p, e in zip(persian_digits, english_digits):
            res = res.replace(p, e)
        return re.sub(r'\D', '', res)

    @property
    def formatted_card_number(self):
        """شماره کارت چهار رقم چهار رقم جدا شده برای نمایش زیبا روی کارت"""
        raw = self.clean_card_number
        if len(raw) == 16:
            return f"{raw[0:4]}  {raw[4:8]}  {raw[8:12]}  {raw[12:16]}"
        return self.card_number


class CafeMusic(models.Model):
    title = models.CharField(max_length=120, verbose_name="نام موزیک")
    artist = models.CharField(max_length=100, blank=True, default="کافه عرفان", verbose_name="نام هنرمند / سبک")
    audio_file = models.FileField(upload_to='music/', verbose_name="فایل صوتی موزیک (mp3)")
    is_active = models.BooleanField(default=True, verbose_name="فعال در پلی‌لیست")
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ بارگذاری")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "موزیک کافه"
        verbose_name_plural = "پلی‌لیست موزیک‌های کافه"

    def __str__(self):
        return f"{self.title} ({self.artist})"


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
