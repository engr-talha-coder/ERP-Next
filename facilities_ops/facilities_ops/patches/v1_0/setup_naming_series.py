import frappe


NAMING_SERIES = {
    "Client Site": "SITE-.YYYY.-.#####",
    "Service Contract": "SC-.YYYY.-.#####",
    "Daily Service Plan": "DSP-.YYYY.-.MM.-.#####",
    "Daily Service Task": "DST-.YYYY.-.#####",
    "Service Request": "SR-.YYYY.-.#####",
    "Client Signoff": "CSO-.YYYY.-.#####",
    "Consumable Consumption Slip": "CCS-.YYYY.-.#####",
    "Fleet Vehicle": "FV-.YYYY.-.#####",
    "Driver": "DRV-.YYYY.-.#####",
    "Trip Request": "TR-.YYYY.-.#####",
    "Trip Sheet": "TS-.YYYY.-.#####",
    "Fuel Log": "FL-.YYYY.-.#####",
    "Monthly Billing Summary": "MBS-.YYYY.-.MM.-.#####",
}


def execute():
    """Seed naming series options for all Facilities Ops doctypes."""
    for doctype, series in NAMING_SERIES.items():
        existing = frappe.db.get_value("DocType", doctype, "autoname") or ""
        if series not in existing:
            frappe.db.set_value("DocType", doctype, "autoname", f"naming_series:")
        _ensure_series_option(doctype, series)
    frappe.db.commit()


def _ensure_series_option(doctype, series):
    """Ensure the naming series value exists in the Series table."""
    if not frappe.db.exists("Series", series):
        frappe.db.sql(
            "INSERT IGNORE INTO `tabSeries` (`name`, `current`) VALUES (%s, 0)",
            (series,),
        )
