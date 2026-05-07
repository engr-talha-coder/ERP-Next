import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class Driver(Document):
    def validate(self):
        self._check_license_expiry()

    def _check_license_expiry(self):
        if self.license_expiry and getdate(self.license_expiry) < getdate(today()):
            frappe.msgprint(
                frappe._("Warning: Driver {0}'s license has expired on {1}.").format(
                    self.full_name, self.license_expiry
                ),
                alert=True,
                indicator="orange",
            )
