import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.models import SiteSettings, LuckyWheelCoupon
from apps.menu.models import MenuCategory, MenuItem
from apps.reservations.models import ReservationSettings
from apps.shop.models import ProductCategory, Product

print("Seeding coffee shop database...")

# 1. Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@cafenovin.ir', 'admin123')
    print("Superuser 'admin' with password 'admin123' created.")

# 2. Site Settings
site, _ = SiteSettings.objects.get_or_create(id=1)
site.site_name = "کافه اسپرسو نوین"
site.tagline = "طعم اصیل دانه برشته و عطر فراتر از انتظار"
site.primary_color = "#E65100"
site.secondary_color = "#121417"
site.open_time = "08:00"
site.close_time = "23:30"
site.phone = "021-88990011"
site.address = "تهران، خیابان ولیعصر، بالاتر از پارک ساعی، پلاک ۱۲۰"
site.instagram = "@novin_coffeebar"
site.save()

# 3. Reservation Settings
res_settings, _ = ReservationSettings.objects.get_or_create(id=1)
res_settings.require_deposit = False
res_settings.deposit_amount = 50000
res_settings.save()

# 4. Lucky Wheel Coupons
coupons = [
    ("COFFEE10", "۱۰٪ تخفیف کل سفارش منو", 10),
    ("FREEBARISTA", "۱ عدد دونات مجانی روی اسپرسو", 15),
    ("VIP20", "۲۰٪ تخفیف اختصاصی مشتریان وفادار", 20),
    ("GIFT50K", "۵۰ هزار تومان بیعانه مهمان کافه", 25),
]
for code, title, pct in coupons:
    LuckyWheelCoupon.objects.get_or_create(code=code, defaults={'title': title, 'discount_percent': pct})

# 5. Menu Categories
cat_espresso, _ = MenuCategory.objects.get_or_create(title="اسپرسو بار (Espresso Bar)", slug="espresso-bar", defaults={'icon': 'mug-hot', 'display_order': 1})
cat_cold, _ = MenuCategory.objects.get_or_create(title="سرد و آیس (Cold Brew & Ice)", slug="cold-drinks", defaults={'icon': 'snowflake', 'display_order': 2})
cat_bakery, _ = MenuCategory.objects.get_or_create(title="شیرینی و کیک برشته (Bakery)", slug="bakery", defaults={'icon': 'cookie-bite', 'display_order': 3})
cat_breakfast, _ = MenuCategory.objects.get_or_create(title="صبحانه و میان‌ویژه", slug="breakfast", defaults={'icon': 'utensils', 'display_order': 4})

# 6. Menu Items
items_data = [
    # Espresso Bar
    (cat_espresso, "دوبل اسپرسو آرتین", "عصاره‌گیری ۱۰۰٪ عربیکا با کِرِمای طلایی عمیق و نت‌های شکلاتی.", 55000, 0, "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=500", "پیشنهاد باریستا", "hot", True),
    (cat_espresso, "کاپوچینو با شیر مخملی", "یک شات اسپرسو غلیظ به همراه فوم شیر مخملی تازه.", 68000, 60000, "https://images.unsplash.com/photo-1534778101976-62847782c213?w=500", "پرفروش", "hot", True),
    (cat_espresso, "کارامل ماکیاتو برشته", "اسپرسو، شیر گرم، فوم شیر و سس کارامل دست‌ساز.", 78000, 70000, "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=500", "محبوب", "hot", False),
    (cat_espresso, "کافه موکا فندقی", "ترکیب اسپرسو، پودر کاکائو غلیظ بلژیکی و عصاره فندق.", 82000, 0, "https://images.unsplash.com/photo-1578314675249-a6910f80cc4e?w=500", "ویژه", "hot", True),

    # Cold Drinks
    (cat_cold, "آیس آمریکانو ماندارین", "اسپرسو عصاره‌گیری سرد به همراه یخ و عصاره مرکبات تازه.", 72000, 65000, "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500", "خنک‌کننده", "cold", True),
    (cat_cold, "آیس لاته وانیلی", "اسپرسو، شیر سرد، یخ و عصاره طبیعی وانیل ماداگاسکار.", 75000, 0, "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=500", "تابستانی", "cold", False),
    (cat_cold, "کلد برو نیتروژن", "دم‌آوری سرد ۱۲ ساعته با گاز نیتروژن و بافت مخملی بی‌نظیر.", 88000, 80000, "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500", "تخصصی", "cold", True),

    # Bakery
    (cat_bakery, "کرواسان شکلات تلخ نوین", "کرواسان داغ و ترد فرانسوی با مغز شکلات ۷۰٪ تلخ.", 65000, 58000, "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500", "تازه داغ", "neutral", True),
    (cat_bakery, "چیزکیک نیویورکی با توت‌فرنگی", "چیزکیک پخته‌شده به روش سنتی نیویورک با سس توت‌فرنگی.", 85000, 0, "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=500", "شیرینی روز", "neutral", False),

    # Breakfast
    (cat_breakfast, "بشقاب صبحانه انگلیسی کامل", "تخم‌مرغ نيمرو، سوسیس گریل، لوبیا گرم، قارچ بلانچ، ژامبون و نان تست.", 185000, 165000, "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=500", "صبحانه ویژه", "neutral", True),
]

for cat, title, desc, price, disc, img_url, badge, temp, feat in items_data:
    MenuItem.objects.get_or_create(
        title=title,
        defaults={
            'category': cat,
            'description': desc,
            'price': price,
            'discount_price': disc,
            'image_url': img_url,
            'badge_text': badge,
            'temperature': temp,
            'is_featured': feat,
            'is_active': True
        }
    )

# 7. Shop Categories & Products
shop_beans, _ = ProductCategory.objects.get_or_create(title="دانه‌های برشته تخصصی", slug="specialty-coffee-beans")
shop_equip, _ = ProductCategory.objects.get_or_create(title="تجهیزات دم‌آوری و اکسسوری", slug="coffee-equipment")

products_data = [
    (shop_beans, "دانه قهوه عربیکا اتيوپی یرگاچف (۲۵۰ گرمی)", "ethiopia-yirgacheffe", "طعم‌یادهای لیمویی، گلی و یاس با اسیدیته روشن و دلپذیر.", 290000, 260000, "light", "لیمو، یاسمن، عسل", 4, 2, "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=500"),
    (shop_beans, "دانه قهوه کلمبیا سوپرمو (۲۵۰ گرمی)", "colombia-supreme", "طعم‌یاد کاراملی، گردویی و شکلات شیری با برشته‌کاری متوسط.", 270000, 0, "medium", "کارامل، فندق، شکلات", 3, 3, "https://images.unsplash.com/photo-1611854779393-1b2da9d400fe?w=500"),
    (shop_beans, "میکس بلند اسپرسو نوین ۷۰/۳۰ (۵۰۰ گرمی)", "novin-espresso-blend-500g", "ترکیب ۷۰٪ عربیکا و ۳۰٪ ربوستا با کرمای غلیظ، تلخی عمیق و کافئین مناسب.", 380000, 340000, "dark", "شکلات تلخ، دود، گردو", 2, 5, "https://images.unsplash.com/photo-1587734195503-904fca47e0e9?w=500"),
    (shop_equip, "موکاپات ۳ کاپ استیل مدرن", "mokapot-3cup-steel", "بدنه استیل ضد زنگ مناسب عصاره‌گیری غلیظ اسپرسو روی اجاق.", 450000, 0, "none", "تجهیزات عصاره‌گیری", 0, 0, "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500"),
]

for cat, title, slug, desc, price, disc, roast, notes, acid, bitter, img_url in products_data:
    Product.objects.get_or_create(
        slug=slug,
        defaults={
            'category': cat,
            'title': title,
            'description': desc,
            'price': price,
            'discount_price': disc,
            'roast_level': roast,
            'flavor_notes': notes,
            'acidity_level': acid,
            'bitterness_level': bitter,
            'image_url': img_url,
            'is_active': True,
            'is_featured': True
        }
    )

print("Seeding completed successfully!")
