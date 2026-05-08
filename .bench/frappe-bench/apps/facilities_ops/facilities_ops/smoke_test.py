"""Smoke tests for facilities_ops installation validation."""

EXPECTED_DOCTYPES = [
    "Client Site",
    "Service Type",
    "Shift Template",
    "Service Checklist Template",
    "Service Checklist Item",
    "Billing Rule",
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
    import frappe

    failures = []

    installed = frappe.get_installed_apps()
    if "facilities_ops" not in installed:
        failures.append("FAIL: facilities_ops not in installed apps")
    else:
        print("[OK] facilities_ops is installed")

    for dt in EXPECTED_DOCTYPES:
        if frappe.db.exists("DocType", dt):
            print(f"[OK] DocType: {dt}")
        else:
            failures.append(f"FAIL: DocType '{dt}' not found")

    for role in EXPECTED_ROLES:
        if frappe.db.exists("Role", role):
            print(f"[OK] Role: {role}")
        else:
            failures.append(f"FAIL: Role '{role}' not found")

    for wf in EXPECTED_WORKFLOWS:
        if frappe.db.exists("Workflow", wf):
            print(f"[OK] Workflow: {wf}")
        else:
            failures.append(f"FAIL: Workflow '{wf}' not found")

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

    print("\n" + "=" * 60)
    if failures:
        print(f"SMOKE TEST FAILED - {len(failures)} issue(s):")
        for item in failures:
            print(f"  {item}")
        raise Exception("Smoke tests failed")

    print("ALL SMOKE TESTS PASSED")
    return "ok"
