import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date, now_datetime


class ServiceRequest(Document):
    def validate(self):
        self._set_sla_deadlines()

    def _set_sla_deadlines(self):
        if self.sla_matrix and self.request_date and not self.response_due:
            sla = frappe.get_doc("SLA Matrix", self.sla_matrix)
            base = self.request_date
            self.response_due = add_to_date(base, hours=sla.response_time_hours)
            self.resolution_due = add_to_date(base, hours=sla.resolution_time_hours)

    def check_sla_breaches(self):
        now = now_datetime()
        if self.status not in ("Resolved", "Closed", "Cancelled"):
            if self.resolution_due and now > self.resolution_due:
                self.db_set("sla_breached", 1)


@frappe.whitelist()
def check_sla_breaches():
    """Scheduler job: mark breached SRs."""
    open_requests = frappe.get_all(
        "Service Request",
        filters={"status": ["not in", ["Resolved", "Closed", "Cancelled"]]},
        fields=["name"],
    )
    for req in open_requests:
        doc = frappe.get_doc("Service Request", req.name)
        doc.check_sla_breaches()
    frappe.db.commit()
