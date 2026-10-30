FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# نصب پیش‌نیازهای سیستمی
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# کپی و نصب وابستگی‌ها
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل سورس پروژه
COPY . /app/

# جمع‌آوری فایل‌های استاتیک در زمان ساخت ایمیج
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# اسکریپت استارت
RUN chmod +x /app/start.sh

CMD ["sh", "/app/start.sh"]
