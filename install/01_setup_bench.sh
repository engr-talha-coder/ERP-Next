#!/usr/bin/env bash
# 01_setup_bench.sh — Install frappe-bench and create a new bench
set -euo pipefail

BENCH_DIR="${BENCH_DIR:-/home/frappe/frappe-bench}"
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"
PYTHON="${PYTHON:-python3}"

echo ">>> Installing bench CLI..."
pip install frappe-bench --quiet

echo ">>> Initialising bench at ${BENCH_DIR} (branch: ${FRAPPE_BRANCH})..."
bench init --frappe-branch "${FRAPPE_BRANCH}" "${BENCH_DIR}"

echo ">>> Configuring developer mode..."
cd "${BENCH_DIR}"
bench set-config -g developer_mode 1

echo ">>> Getting ERPNext app..."
bench get-app --branch version-15 erpnext

echo ">>> Bench setup complete. Path: ${BENCH_DIR}"
