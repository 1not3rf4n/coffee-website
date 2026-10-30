import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# فایل .env رو از ریشه پروژه لود کن
load_dotenv(BASE_DIR / '.env')

# ---------------------------------------------------------------------------
# Security — در production حتماً SECRET_KEY رو از environment variable بخون
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-coffee-luxury-secret-key-antigravity-mode'  # فقط برای dev
)

# در حین بالا آوردن اولیه True می‌ذاریم تا خطاهای احتمالی لاگ بشن
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
    'https://*.htempurl.com',
    'http://*.htempurl.com',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'jazzmin',   # modern themed admin — must sit above django.contrib.admin

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Coffee Shop Apps
    'apps.core',
    'apps.menu',
    'apps.reservations',
    'apps.shop',
    'apps.cart',
    'apps.orders',
    'apps.dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise — باید بلافاصله بعد از SecurityMiddleware باشه
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise — فشرده‌سازی و cache فایل‌های استاتیک در production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ---------------------------------------------------------------------------
# Production Security Headers
# ---------------------------------------------------------------------------
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SESSION_COOKIE_SECURE = False   # اگه SSL دارید True کنید
    CSRF_COOKIE_SECURE = False       # اگه SSL دارید True کنید

# Auth redirects — the staff /management/ dashboard and admin share Django login.
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/management/'
LOGOUT_REDIRECT_URL = '/'

# ---------------------------------------------------------------------------
# Jazzmin — themed Django admin (RTL, Persian, coffee-brand orange)
# ---------------------------------------------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "پنل مدیریت نوین کافه",
    "site_header": "نوین کافه",
    "site_brand": "نوین کافه",
    "site_logo": None,
    "login_logo": None,
    "site_icon": None,
    "welcome_sign": "به پنل مدیریت نوین کافه خوش آمدید ☕",
    "copyright": "نوین کافه",
    "search_model": ["orders.Order", "shop.Product"],

    # Top menu links
    "topmenu_links": [
        {"name": "مشاهده سایت", "url": "/", "new_window": True},
        {"name": "پنل مدیریت سریع", "url": "/management/", "new_window": False},
        {"app": "orders"},
        {"app": "shop"},
    ],

    # FontAwesome icons per model (fa 6 free set ships with jazzmin)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "orders.Order": "fas fa-receipt",
        "orders.OrderItem": "fas fa-box",
        "shop.Product": "fas fa-mug-hot",
        "shop.ProductCategory": "fas fa-tags",
        "menu.MenuItem": "fas fa-coffee",
        "menu.MenuCategory": "fas fa-list",
        "reservations.TableReservation": "fas fa-chair",
        "reservations.ReservationSettings": "fas fa-cog",
        "core.SiteSettings": "fas fa-sliders-h",
        "core.LuckyWheelCoupon": "fas fa-ticket-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # Order of apps/models in the sidebar — orders & shop first (most used)
    "order_with_respect_to": [
        "orders", "shop", "menu", "reservations", "core", "auth",
    ],

    "related_modal_active": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "core.sitesettings": "collapsible",
    },
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-warning",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
