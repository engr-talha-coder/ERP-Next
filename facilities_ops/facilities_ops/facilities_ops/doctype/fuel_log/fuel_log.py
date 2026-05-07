import frappe
from frappe.model.document import Document


class FuelLog(Document):
    def validate(self):
        if self.quantity_litres and self.price_per_litre:
            self.total_cost = round(self.quantity_litres * self.price_per_litre, 2)
        if self.odometer_reading and self.vehicle:
            current = frappe.db.get_value(
                "Fleet Vehicle", self.vehicle, "odometer_reading"
            ) or 0
            if self.odometer_reading < current:
                frappe.throw(
                    frappe._(
                        "Odometer reading {0} km is less than the vehicle's current reading {1} km."
                    ).format(self.odometer_reading, current)
                )
