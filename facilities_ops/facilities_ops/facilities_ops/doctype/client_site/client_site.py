import frappe
from frappe.model.document import Document


class ClientSite(Document):
    def validate(self):
        self._validate_geo_coordinates()

    def _validate_geo_coordinates(self):
        if self.geo_coordinates:
            parts = self.geo_coordinates.split(",")
            if len(parts) != 2:
                frappe.throw(
                    frappe._("Geo Coordinates must be in 'latitude, longitude' format.")
                )
            try:
                lat, lng = float(parts[0].strip()), float(parts[1].strip())
            except ValueError:
                frappe.throw(frappe._("Geo Coordinates must contain numeric latitude and longitude."))
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                frappe.throw(frappe._("Geo Coordinates are out of valid range."))
