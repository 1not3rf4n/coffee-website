import os
import sys

# مسیر ریشه پروژه
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# معرفی تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# اجرای مایگریشن‌های پایگاه داده در صورت نیاز
try:
    import django
    django.setup()
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    pass

# اجرای جنگو
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
