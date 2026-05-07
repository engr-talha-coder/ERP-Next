import frappe
from frappe.model.document import Document


class SlaMatrix(Document):
    def validate(self):
        if self.response_time_hours and self.resolution_time_hours:
            if self.response_time_hours >= self.resolution_time_hours:
                frappe.throw(
                    frappe._("Response Time must be less than Resolution Time.")
                )
        if self.escalation_time_hours and self.resolution_time_hours:
            if self.escalation_time_hours > self.resolution_time_hours:
                frappe.throw(
                    frappe._("Escalation Time should not exceed Resolution Time.")
                )
