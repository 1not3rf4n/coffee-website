from django.db import models

class ProductCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان دسته")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "دسته‌بندی فروشگاه"
        verbose_name_plural = "دسته‌بندی‌های فروشگاه"

    def __str__(self):
        return self.title

class Product(models.Model):
    ROAST_CHOICES = (
        ('light', 'برشته‌کاری سبک (Light Roast)'),
        ('medium', 'برشته‌کاری متوسط (Medium Roast)'),
        ('dark', 'برشته‌کاری تیره (Dark Roast)'),
        ('none', 'غیر دانه‌ای / تجهیزات'),
    )

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', verbose_name="دسته‌بندی")
    title = models.CharField(max_length=150, verbose_name="نام محصول")
    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات محصول")
    price = models.IntegerField(verbose_name="قیمت (تومان)")
    discount_price = models.IntegerField(default=0, verbose_name="قیمت تخفیف‌خورده (تومان)")
    
    image = models.ImageField(upload_to='shop/', blank=True, null=True, verbose_name="تصویر اصلی")
    image_url = models.CharField(max_length=500, blank=True, null=True, verbose_name="لینک تصویر fallback")
    
    stock = models.IntegerField(default=20, verbose_name="موجودی انبار")
    roast_level = models.CharField(max_length=20, choices=ROAST_CHOICES, default='medium', verbose_name="میزان برشته‌کاری")
    flavor_notes = models.CharField(max_length=200, blank=True, verbose_name="طعم‌یادها (مثال: شکلاتی، کاراملی، فندقی)")
    acidity_level = models.IntegerField(default=3, verbose_name="میزان اسیدیته (۱ تا ۵)")
    bitterness_level = models.IntegerField(default=3, verbose_name="میزان تلخی (۱ تا ۵)")
    
    is_active = models.BooleanField(default=True, verbose_name="فعال / موجود")
    is_featured = models.BooleanField(default=False, verbose_name="محصول ویژه / پرفروش")

    class Meta:
        verbose_name = "محصول فروشگاه"
        verbose_name_plural = "محصولات فروشگاه"

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
