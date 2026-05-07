#!/usr/bin/env bash
# 02_create_site.sh — Create a new Frappe site
set -euo pipefail

BENCH_DIR="${BENCH_DIR:-/home/frappe/frappe-bench}"
SITE_NAME="${SITE_NAME:-facilities.local}"
DB_ROOT_PASSWORD="${DB_ROOT_PASSWORD:-}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"

cd "${BENCH_DIR}"

echo ">>> Creating site: ${SITE_NAME}..."
if [ -n "${DB_ROOT_PASSWORD}" ]; then
    bench new-site "${SITE_NAME}" \
        --db-root-password "${DB_ROOT_PASSWORD}" \
        --admin-password "${ADMIN_PASSWORD}"
else
    bench new-site "${SITE_NAME}" \
        --admin-password "${ADMIN_PASSWORD}"
fi

echo ">>> Setting default site..."
bench use "${SITE_NAME}"

echo ">>> Site '${SITE_NAME}' created successfully."
