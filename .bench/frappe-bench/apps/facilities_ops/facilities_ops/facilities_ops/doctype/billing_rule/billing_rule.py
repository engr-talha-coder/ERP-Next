import frappe
from frappe.model.document import Document


class BillingRule(Document):
    def validate(self):
        if self.rate and self.rate <= 0:
            frappe.throw(frappe._("Rate must be greater than zero."))
        if self.overtime_rate and self.overtime_rate < self.rate:
            frappe.throw(frappe._("Overtime Rate should not be less than the base Rate."))
