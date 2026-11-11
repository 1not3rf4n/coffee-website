import re
from django import template

register = template.Library()

@register.filter(name='price_format')
def price_format(value):
    """جداکننده سه رقم سه رقم قیمت‌ها: 150000 -> 150,000"""
    if value is None or value == '':
        return '0'
    try:
        val = int(value)
        return f"{val:,}"
    except (ValueError, TypeError):
        return str(value)

@register.filter(name='toman')
def toman(value):
    """فرمت کامل قیمت به همراه کلمه تومان: 150000 -> 150,000 تومان"""
    formatted = price_format(value)
    return f"{formatted} تومان"

@register.filter(name='card_split')
def card_split(value):
    """جدا کردن ۴ رقم ۴ رقم شماره کارت جهت نمایش فوق‌العاده شیک"""
    if not value:
        return ""
    digits = re.sub(r'\D', '', str(value))
    if len(digits) == 16:
        return f"{digits[0:4]}  {digits[4:8]}  {digits[8:12]}  {digits[12:16]}"
    return str(value)

@register.filter(name='clean_phone')
def clean_phone(value):
    """شماره تماس تمیز برای لینک tel:"""
    if not value:
        return ""
    return re.sub(r'[^\d+]', '', str(value))

@register.filter(name='clean_insta')
def clean_insta(value):
    """آیدی تمیز اینستاگرام برای لینک مستقیم پیج"""
    if not value:
        return ""
    val = str(value).strip()
    if 'instagram.com/' in val:
        val = val.split('instagram.com/')[-1].split('/')[0].split('?')[0]
    return val.lstrip('@')
