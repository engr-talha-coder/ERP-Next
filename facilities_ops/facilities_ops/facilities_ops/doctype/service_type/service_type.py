import frappe
from frappe.model.document import Document


class ServiceType(Document):
    def validate(self):
        if self.default_response_hours and self.default_resolution_hours:
            if self.default_response_hours >= self.default_resolution_hours:
                frappe.throw(
                    frappe._("Default Response Hours must be less than Default Resolution Hours.")
                )
