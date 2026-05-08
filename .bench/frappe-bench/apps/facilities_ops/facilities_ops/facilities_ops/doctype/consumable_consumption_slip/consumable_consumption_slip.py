import frappe
from frappe.model.document import Document


class ConsumableConsumptionSlip(Document):
    def validate(self):
        self._calculate_totals()

    def on_submit(self):
        self.status = "Submitted"
        self.db_set("status", "Submitted")
        self._post_stock_entry()

    def on_cancel(self):
        self.status = "Cancelled"
        self.db_set("status", "Cancelled")

    def _calculate_totals(self):
        total = sum(row.amount or 0 for row in self.consumption_items)
        self.total_amount = total

    def _post_stock_entry(self):
        if not self.warehouse:
            return
        se = frappe.get_doc(
            {
                "doctype": "Stock Entry",
                "stock_entry_type": "Material Issue",
                "posting_date": self.posting_date,
                "from_warehouse": self.warehouse,
                "items": [
                    {
                        "item_code": row.item_code,
                        "qty": row.quantity,
                        "uom": row.uom,
                        "basic_rate": row.rate,
                    }
                    for row in self.consumption_items
                    if row.item_code
                ],
            }
        )
        se.insert(ignore_permissions=True)
        se.submit()
        frappe.msgprint(
            frappe._("Stock Entry {0} created.").format(
                frappe.utils.get_link_to_form("Stock Entry", se.name)
            )
        )



