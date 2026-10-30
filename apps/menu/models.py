from django.db import models

class MenuCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان دسته")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    icon = models.CharField(max_length=50, default="coffee", verbose_name="آیکون (FontAwesome/SVG)")
    display_order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال / روشن")

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "دسته‌بندی منو"
        verbose_name_plural = "دسته‌بندی‌های منو"

    def __str__(self):
        return self.title

class MenuItem(models.Model):
    TEMP_CHOICES = (
        ('hot', 'گرم'),
        ('cold', 'سرد'),
        ('neutral', 'معمولی / خوراکی'),
    )

    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items', verbose_name="دسته‌بندی")
    title = models.CharField(max_length=150, verbose_name="نام آیتم")
    description = models.TextField(blank=True, verbose_name="توضیحات و ترکیبات")
    price = models.IntegerField(verbose_name="قیمت اصلی (تومان)")
    discount_price = models.IntegerField(default=0, verbose_name="قیمت با تخفیف (تومان - صفر یعنی بدون تخفیف)")
    
    image = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name="تصویر آیتم")
    image_url = models.CharField(max_length=500, blank=True, null=True, verbose_name="لینک تصویر fallback")
    
    display_order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="موجود / روشن")
    is_featured = models.BooleanField(default=False, verbose_name="پیشنهاد ویژه باریستا")
    badge_text = models.CharField(max_length=50, blank=True, verbose_name="نشان اختصاصی (مثلا: ویژه، پرفروش، رژیمی)")
    temperature = models.CharField(max_length=10, choices=TEMP_CHOICES, default='hot', verbose_name="نوع سرو")

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "آیتم منو"
        verbose_name_plural = "آیتم‌های منو"

    def __str__(self):
        return f"{self.title} - {self.price} تومان"

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or '/static/images/default-coffee.jpg'

    @property
    def final_price(self):
        if self.discount_price and 0 < self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def discount_percent(self):
        if self.discount_price and 0 < self.discount_price < self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
