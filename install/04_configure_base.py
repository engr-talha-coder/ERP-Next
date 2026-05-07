#!/usr/bin/env python3
"""
04_configure_base.py — Bootstrap base configuration for facilities_ops.
Run via: bench --site <site> execute facilities_ops.install.configure_base
Or directly: python 04_configure_base.py <site>
"""
import sys
import os


def configure(site=None):
    """Set up base configuration using the Frappe API."""
    # Locate bench root
    bench_path = os.environ.get("BENCH_PATH", os.path.expanduser("~/frappe-bench"))
    sys.path.insert(0, os.path.join(bench_path, "apps", "frappe"))
    sys.path.insert(0, os.path.join(bench_path, "apps", "erpnext"))
    sys.path.insert(0, os.path.join(bench_path, "apps", "facilities_ops"))

    import frappe

    site = site or os.environ.get("FRAPPE_SITE", "facilities.local")
    frappe.init(site=site, sites_path=os.path.join(bench_path, "sites"))
    frappe.connect()

    try:
        _setup_system_settings()
        _setup_naming_series()
        frappe.db.commit()
        print("[OK] Base configuration applied successfully.")
    finally:
        frappe.destroy()


def _setup_system_settings():
    import frappe

    ss = frappe.get_single("System Settings")
    if not ss.country:
        ss.country = "South Africa"
    ss.language = "en"
    ss.save(ignore_permissions=True)
    print("[OK] System Settings updated.")


def _setup_naming_series():
    import frappe

    series_map = {
        "Client Site": "SITE-.YYYY.-.#####\n",
        "Service Contract": "SC-.YYYY.-.#####\n",
        "Daily Service Plan": "DSP-.YYYY.-.MM.-.#####\n",
        "Daily Service Task": "DST-.YYYY.-.#####\n",
        "Service Request": "SR-.YYYY.-.#####\n",
        "Client Signoff": "CSO-.YYYY.-.#####\n",
        "Consumable Consumption Slip": "CCS-.YYYY.-.#####\n",
        "Fleet Vehicle": "FV-.YYYY.-.#####\n",
        "Driver": "DRV-.YYYY.-.#####\n",
        "Trip Request": "TR-.YYYY.-.#####\n",
        "Trip Sheet": "TS-.YYYY.-.#####\n",
        "Fuel Log": "FL-.YYYY.-.#####\n",
        "Monthly Billing Summary": "MBS-.YYYY.-.MM.-.#####\n",
    }
    for doctype, options in series_map.items():
        meta = frappe.get_meta(doctype)
        field = meta.get_field("naming_series")
        if field:
            current_opts = field.options or ""
            for opt in options.strip().split("\n"):
                if opt not in current_opts:
                    current_opts += "\n" + opt
            frappe.db.set_value(
                "DocField",
                {"parent": doctype, "fieldname": "naming_series"},
                "options",
                current_opts.strip(),
            )
    print("[OK] Naming series configured.")


if __name__ == "__main__":
    site_arg = sys.argv[1] if len(sys.argv) > 1 else None
    configure(site_arg)
