import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours


class DailyServiceTask(Document):
    def validate(self):
        self._validate_mandatory_checklist()
        self._calculate_duration()

    def on_submit(self):
        if self.status not in ("Completed", "Missed"):
            frappe.throw(
                frappe._("Task must be Completed or Missed before submission.")
            )

    def _validate_mandatory_checklist(self):
        for row in self.checklist_responses:
            if row.is_mandatory and not row.response:
                frappe.throw(
                    frappe._("Mandatory checklist item '{0}' has no response.").format(
                        row.item_description
                    )
                )

    def _calculate_duration(self):
        if self.actual_start_time and self.actual_end_time:
            hours = time_diff_in_hours(self.actual_end_time, self.actual_start_time)
            if hours < 0:
                frappe.throw(frappe._("Actual End Time must be after Actual Start Time."))
            self.actual_duration_hours = round(hours, 2)
