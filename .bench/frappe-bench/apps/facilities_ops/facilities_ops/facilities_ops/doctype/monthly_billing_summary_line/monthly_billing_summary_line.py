from frappe.model.document import Document


class MonthlyBillingSummaryLine(Document):
    def validate(self):
        if self.quantity and self.unit_rate:
            self.line_total = self.quantity * self.unit_rate
        if self.line_total and self.tax_rate:
            self.tax_amount = round(self.line_total * self.tax_rate / 100, 2)
