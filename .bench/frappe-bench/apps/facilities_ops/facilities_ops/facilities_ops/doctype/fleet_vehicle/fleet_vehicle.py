import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days, getdate


EXPIRY_ALERT_DAYS = 30


class FleetVehicle(Document):
    def validate(self):
        self._validate_year()

    def _validate_year(self):
        import datetime
        current_year = datetime.date.today().year
        if self.year and not (1900 <= self.year <= current_year + 1):
            frappe.throw(frappe._("Vehicle year {0} is not valid.").format(self.year))


@frappe.whitelist()
def check_document_expiry():
    """Scheduler job: send alerts for expiring vehicle documents."""
    alert_threshold = add_days(today(), EXPIRY_ALERT_DAYS)
    vehicles = frappe.get_all(
        "Fleet Vehicle",
        filters={"active": 1},
        fields=["name", "registration_number", "insurance_expiry", "road_tax_expiry", "inspection_expiry"],
    )
    for v in vehicles:
        for field, label in [
            ("insurance_expiry", "Insurance"),
            ("road_tax_expiry", "Road Tax"),
            ("inspection_expiry", "Inspection"),
        ]:
            expiry = v.get(field)
            if expiry and getdate(expiry) <= getdate(alert_threshold):
                frappe.sendmail(
                    recipients=frappe.db.get_single_value("System Settings", "email_footer_address")
                    or "admin@facilitiesops.com",
                    subject=frappe._("{0} Expiry Alert: {1}").format(label, v.registration_number),
                    message=frappe._(
                        "Vehicle {0} {1} expires on {2}."
                    ).format(v.registration_number, label, expiry),
                )
    frappe.db.commit()
