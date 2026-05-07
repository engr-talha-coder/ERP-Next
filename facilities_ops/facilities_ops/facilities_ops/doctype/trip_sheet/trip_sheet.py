import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours


class TripSheet(Document):
    def validate(self):
        self._calculate_km()
        self._calculate_duration()
        self._update_vehicle_odometer()

    def on_submit(self):
        self.status = "Completed"
        self.db_set("status", "Completed")
        self._update_driver_stats()

    def _calculate_km(self):
        if self.odometer_end and self.odometer_start:
            if self.odometer_end < self.odometer_start:
                frappe.throw(frappe._("Odometer End must be greater than Odometer Start."))
            self.total_km = self.odometer_end - self.odometer_start

    def _calculate_duration(self):
        if self.actual_departure and self.actual_return:
            hours = time_diff_in_hours(self.actual_return, self.actual_departure)
            if hours < 0:
                frappe.throw(frappe._("Actual Return must be after Actual Departure."))
            self.trip_duration_hours = round(hours, 2)

    def _update_vehicle_odometer(self):
        if self.odometer_end and self.vehicle:
            frappe.db.set_value("Fleet Vehicle", self.vehicle, "odometer_reading", self.odometer_end)

    def _update_driver_stats(self):
        if not self.driver:
            return
        driver = frappe.get_doc("Driver", self.driver)
        driver.total_trips = (driver.total_trips or 0) + 1
        driver.total_km_driven = (driver.total_km_driven or 0) + (self.total_km or 0)
        driver.db_update()



