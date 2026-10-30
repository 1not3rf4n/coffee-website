from django.db import models
from apps.shop.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده / در حال آماده‌سازی'),
        ('processing', 'در حال پردازش و برشته‌کاری'),
        ('shipped', 'تحویل پست / ارسال شده'),
        ('cancelled', 'لغو شده'),
    )

    order_number = models.CharField(max_length=50, unique=True, verbose_name="شماره سفارش")
    full_name = models.CharField(max_length=100, verbose_name="نام خریدار")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس تحویل")
    total_price = models.IntegerField(verbose_name="مبلغ کل (تومان)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت سفارش")
    payment_gateway = models.CharField(max_length=50, default='زرین‌پال', verbose_name="درگاه پرداخت")
    tracking_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="کد پیگیری پرداخت / مرسوله")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "سفارش فروشگاه"
        verbose_name_plural = "سفارشات فروشگاه"

    def __str__(self):
        return f"سفارش {self.order_number} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="محصول")
    product_name = models.CharField(max_length=150, verbose_name="نام محصول")
    price = models.IntegerField(verbose_name="قیمت واحد (تومان)")
    quantity = models.IntegerField(default=1, verbose_name="تعداد")
    grind_type = models.CharField(max_length=50, default="دانه کامل", verbose_name="نوع آسیاب")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def total_item_price(self):
        return self.price * self.quantity
