#!/usr/bin/env python3
"""
smoke_test.py — Verify that the facilities_ops app is installed and all
DocTypes, roles, and workflows exist.

Usage:
    bench --site <site> execute facilities_ops.facilities_ops.smoke_test.run_smoke_tests
    # or
    python scripts/smoke_test.py
"""
import sys
import os


EXPECTED_DOCTYPES = [
    "Client Site",
    "Service Type",
    "Shift Template",
    "Service Checklist Template",
    "Service Checklist Item",
    "Billing Rule",
    "SLA Matrix",
    "Service Contract",
    "Service Contract Line",
    "Daily Service Plan",
    "Daily Service Plan Line",
    "Daily Service Task",
    "Daily Service Task Checklist Response",
    "Service Request",
    "Client Signoff",
    "Consumable Consumption Slip",
    "Consumable Consumption Item",
    "Fleet Vehicle",
    "Driver",
    "Trip Request",
    "Trip Sheet",
    "Fuel Log",
    "Monthly Billing Summary",
    "Monthly Billing Summary Line",
]

EXPECTED_ROLES = [
    "Operations Manager",
    "Operations Planner",
    "Site Supervisor",
    "Transport Coordinator",
    "Fleet Manager",
    "Driver",
    "Client Portal User",
]

EXPECTED_WORKFLOWS = [
    "Service Contract Workflow",
    "Daily Service Plan Workflow",
    "Service Request Workflow",
    "Trip Request Workflow",
    "Monthly Billing Summary Workflow",
]


def run_smoke_tests():
    bench_path = os.environ.get("BENCH_PATH", os.path.expanduser("~/frappe-bench"))
    sys.path.insert(0, os.path.join(bench_path, "apps", "frappe"))
    sys.path.insert(0, os.path.join(bench_path, "apps", "erpnext"))
    sys.path.insert(0, os.path.join(bench_path, "apps", "facilities_ops"))

    import frappe

    site = os.environ.get("FRAPPE_SITE", "facilities.local")
    frappe.init(site=site, sites_path=os.path.join(bench_path, "sites"))
    frappe.connect()

    failures = []

    try:
        # Check app registration
        installed = frappe.get_installed_apps()
        if "facilities_ops" not in installed:
            failures.append("FAIL: facilities_ops not in installed apps")
        else:
            print("[OK] facilities_ops is installed")

        # Check DocTypes
        for dt in EXPECTED_DOCTYPES:
            if frappe.db.exists("DocType", dt):
                print(f"[OK] DocType: {dt}")
            else:
                failures.append(f"FAIL: DocType '{dt}' not found")

        # Check Roles
        for role in EXPECTED_ROLES:
            if frappe.db.exists("Role", role):
                print(f"[OK] Role: {role}")
            else:
                failures.append(f"FAIL: Role '{role}' not found")

        # Check Workflows
        for wf in EXPECTED_WORKFLOWS:
            if frappe.db.exists("Workflow", wf):
                print(f"[OK] Workflow: {wf}")
            else:
                failures.append(f"FAIL: Workflow '{wf}' not found")

        # Check custom fields
        custom_fields = [
            ("Employee", "default_client_site"),
            ("Employee", "service_role"),
            ("Asset", "client_site"),
            ("Asset", "asset_barcode"),
        ]
        for dt, fn in custom_fields:
            if frappe.db.exists("Custom Field", {"dt": dt, "fieldname": fn}):
                print(f"[OK] Custom Field: {dt}.{fn}")
            else:
                failures.append(f"FAIL: Custom Field '{dt}.{fn}' not found")

    finally:
        frappe.destroy()

    print("\n" + "=" * 60)
    if failures:
        print(f"SMOKE TEST FAILED — {len(failures)} issue(s):")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    else:
        print("ALL SMOKE TESTS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    run_smoke_tests()
