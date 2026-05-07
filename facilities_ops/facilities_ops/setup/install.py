import frappe


def after_install():
    """Run after app installation to create base masters."""
    create_departments()
    create_item_groups()
    create_uom()
    frappe.db.commit()


def create_departments():
    departments = [
        "Facilities Operations",
        "Transport & Fleet",
        "Site Management",
        "Billing & Finance",
    ]
    for dept in departments:
        if not frappe.db.exists("Department", dept):
            doc = frappe.get_doc(
                {
                    "doctype": "Department",
                    "department_name": dept,
                    "is_group": 0,
                }
            )
            doc.insert(ignore_permissions=True)


def create_item_groups():
    groups = [
        {"item_group_name": "Consumables", "parent_item_group": "All Item Groups"},
        {"item_group_name": "Cleaning Supplies", "parent_item_group": "Consumables"},
        {"item_group_name": "Safety Equipment", "parent_item_group": "Consumables"},
        {"item_group_name": "Fuel", "parent_item_group": "All Item Groups"},
    ]
    for grp in groups:
        if not frappe.db.exists("Item Group", grp["item_group_name"]):
            doc = frappe.get_doc(
                {
                    "doctype": "Item Group",
                    "item_group_name": grp["item_group_name"],
                    "parent_item_group": grp["parent_item_group"],
                    "is_group": 0,
                }
            )
            doc.insert(ignore_permissions=True)


def create_uom():
    uoms = ["Litre", "Piece", "Box", "Roll", "Bag", "Kg"]
    for uom in uoms:
        if not frappe.db.exists("UOM", uom):
            doc = frappe.get_doc({"doctype": "UOM", "uom_name": uom})
            doc.insert(ignore_permissions=True)
