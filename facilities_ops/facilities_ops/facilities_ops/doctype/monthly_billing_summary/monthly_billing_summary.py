import frappe
from frappe.model.document import Document


class MonthlyBillingSummary(Document):
    def validate(self):
        self._calculate_totals()

    def on_submit(self):
        self.status = "Approved"
        self.db_set("status", "Approved")

    def _calculate_totals(self):
        subtotal = sum(line.line_total or 0 for line in self.billing_lines)
        self.subtotal = subtotal
        tax = sum(line.tax_amount or 0 for line in self.billing_lines)
        self.tax_amount = tax
        self.grand_total = subtotal + tax - (self.discount_amount or 0)

    @frappe.whitelist()
    def create_sales_invoice(self):
        if self.sales_invoice:
            frappe.throw(frappe._("Sales Invoice {0} already exists.").format(self.sales_invoice))

        si = frappe.get_doc(
            {
                "doctype": "Sales Invoice",
                "customer": self.customer,
                "posting_date": frappe.utils.today(),
                "due_date": frappe.utils.add_days(frappe.utils.today(), 30),
                "items": [
                    {
                        "item_code": line.item_code,
                        "item_name": line.description,
                        "qty": line.quantity,
                        "rate": line.unit_rate,
                        "amount": line.line_total,
                    }
                    for line in self.billing_lines
                    if line.item_code
                ],
            }
        )
        si.insert(ignore_permissions=True)
        self.db_set("sales_invoice", si.name)
        self.db_set("invoice_date", si.posting_date)
        self.db_set("status", "Invoiced")
        frappe.msgprint(
            frappe._("Sales Invoice {0} created.").format(
                frappe.utils.get_link_to_form("Sales Invoice", si.name)
            )
        )
        return si.name
