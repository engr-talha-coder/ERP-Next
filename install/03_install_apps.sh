#!/usr/bin/env bash
# 03_install_apps.sh — Install ERPNext and facilities_ops on the site
set -euo pipefail

BENCH_DIR="${BENCH_DIR:-/home/frappe/frappe-bench}"
SITE_NAME="${SITE_NAME:-facilities.local}"
APP_PATH="${APP_PATH:-/home/runner/work/ERP-Next/ERP-Next/facilities_ops}"

cd "${BENCH_DIR}"

echo ">>> Installing ERPNext on ${SITE_NAME}..."
bench --site "${SITE_NAME}" install-app erpnext

echo ">>> Adding facilities_ops app to bench..."
if [ ! -d "apps/facilities_ops" ]; then
    bench get-app facilities_ops "${APP_PATH}"
fi

echo ">>> Installing facilities_ops on ${SITE_NAME}..."
bench --site "${SITE_NAME}" install-app facilities_ops

echo ">>> Running migrate..."
bench --site "${SITE_NAME}" migrate

echo ">>> App installation complete."
