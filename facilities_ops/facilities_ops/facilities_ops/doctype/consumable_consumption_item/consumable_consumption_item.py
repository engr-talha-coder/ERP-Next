from frappe.model.document import Document


class ConsumableConsumptionItem(Document):
    def validate(self):
        if self.quantity and self.rate:
            self.amount = self.quantity * self.rate
