#!/bin/sh
set -e

# اضافه کردن مسیر مجازی‌ساز به PATH در صورت وجود
if [ -d "/app/.venv/bin" ]; then
    export PATH="/app/.venv/bin:$PATH"
fi

# پیدا کردن مفسر پایتون
PYTHON="python"
if ! command -v python >/dev/null 2>&1; then
    PYTHON="python3"
fi

echo "==> Using Python at: $(which $PYTHON)"

echo "==> Running database migrations..."
$PYTHON manage.py migrate --noinput || true

echo "==> Collecting static files..."
$PYTHON manage.py collectstatic --noinput || true

PORT="${PORT:-8000}"
echo "==> Starting Gunicorn on 0.0.0.0:$PORT..."
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

