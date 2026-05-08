import frappe
from frappe.model.document import Document


class TripRequest(Document):
    def validate(self):
        self._validate_dates()
        self._check_vehicle_availability()

    def on_submit(self):
        self.status = "Approved"
        self.db_set("status", "Approved")

    def _validate_dates(self):
        if self.departure_datetime and self.return_datetime:
            if self.return_datetime <= self.departure_datetime:
                frappe.throw(
                    frappe._("Return Date & Time must be after Departure Date & Time.")
                )

    def _check_vehicle_availability(self):
        if not self.vehicle:
            return
        vehicle_doc = frappe.get_doc("Fleet Vehicle", self.vehicle)
        if vehicle_doc.status == "Under Maintenance":
            frappe.throw(
                frappe._("Vehicle {0} is Under Maintenance and cannot be assigned.").format(
                    self.vehicle
                )
            )
