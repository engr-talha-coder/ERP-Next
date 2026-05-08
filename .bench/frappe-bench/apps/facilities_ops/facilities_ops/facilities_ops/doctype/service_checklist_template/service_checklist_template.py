import frappe
from frappe.model.document import Document


class ServiceChecklistTemplate(Document):
    def validate(self):
        if not self.checklist_items:
            frappe.throw(frappe._("At least one Checklist Item is required."))
        self._validate_item_order()

    def _validate_item_order(self):
        seen = set()
        for item in self.checklist_items:
            key = item.item_description
            if key in seen:
                frappe.throw(
                    frappe._("Duplicate checklist item: {0}").format(key)
                )
            seen.add(key)
