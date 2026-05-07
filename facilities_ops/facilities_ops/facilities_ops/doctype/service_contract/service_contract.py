import frappe
from frappe.model.document import Document


class ServiceContract(Document):
    def validate(self):
        self._validate_dates()
        self._calculate_total()

    def on_submit(self):
        self.status = "Active"
        self.db_set("status", "Active")

    def on_cancel(self):
        self.status = "Terminated"
        self.db_set("status", "Terminated")

    def _validate_dates(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                frappe.throw(frappe._("End Date must be after Start Date."))
        if self.renewal_date and self.end_date:
            if self.renewal_date < self.end_date:
                frappe.throw(
                    frappe._("Renewal Date should not be before End Date.")
                )

    def _calculate_total(self):
        total = sum(line.line_total or 0 for line in self.contract_lines)
        self.total_contract_value = total
