from frappe.model.document import Document


class ServiceContractLine(Document):
    def validate(self):
        if self.quantity and self.unit_rate:
            self.line_total = self.quantity * self.unit_rate
