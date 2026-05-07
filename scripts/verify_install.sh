#!/usr/bin/env bash
# verify_install.sh — Verify the bench environment and app installation
set -euo pipefail

BENCH_DIR="${BENCH_DIR:-/home/frappe/frappe-bench}"
SITE_NAME="${SITE_NAME:-facilities.local}"

echo "============================================================"
echo "  facilities_ops Installation Verifier"
echo "============================================================"

# Check bench binary
if ! command -v bench &>/dev/null; then
    echo "[FAIL] bench command not found. Run install/01_setup_bench.sh first."
    exit 1
fi
echo "[OK] bench command found: $(bench --version 2>&1 | head -1)"

# Check bench directory
if [ ! -d "${BENCH_DIR}" ]; then
    echo "[FAIL] Bench directory not found: ${BENCH_DIR}"
    exit 1
fi
echo "[OK] Bench directory: ${BENCH_DIR}"

cd "${BENCH_DIR}"

# Check site exists
if [ ! -d "sites/${SITE_NAME}" ]; then
    echo "[FAIL] Site not found: ${SITE_NAME}"
    exit 1
fi
echo "[OK] Site: ${SITE_NAME}"

# Check ERPNext is installed
ERPNEXT_INSTALLED=$(bench --site "${SITE_NAME}" list-apps 2>/dev/null | grep -c "erpnext" || true)
if [ "${ERPNEXT_INSTALLED}" -eq 0 ]; then
    echo "[FAIL] erpnext not installed on site"
    exit 1
fi
echo "[OK] erpnext installed"

# Check facilities_ops is installed
FAC_INSTALLED=$(bench --site "${SITE_NAME}" list-apps 2>/dev/null | grep -c "facilities_ops" || true)
if [ "${FAC_INSTALLED}" -eq 0 ]; then
    echo "[FAIL] facilities_ops not installed on site"
    exit 1
fi
echo "[OK] facilities_ops installed"

# Run Python smoke test
echo ""
echo ">>> Running Python smoke tests..."
bench --site "${SITE_NAME}" execute "facilities_ops.smoke_test.run_smoke_tests" || {
    echo "[FAIL] Smoke tests failed. See output above."
    exit 1
}

echo ""
echo "============================================================"
echo "  All verification checks passed!"
echo "============================================================"
