import frappe
from frappe.model.document import Document


class ClientSignoff(Document):
    def validate(self):
        if self.signoff_datetime and self.service_date:
            from frappe.utils import getdate, get_datetime
            if getdate(self.signoff_datetime) < getdate(self.service_date):
                frappe.throw(
                    frappe._("Sign-off Date cannot be before Service Date.")
                )
