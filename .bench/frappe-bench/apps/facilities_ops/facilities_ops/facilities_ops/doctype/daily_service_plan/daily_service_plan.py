import frappe
from frappe.model.document import Document


class DailyServicePlan(Document):
    def validate(self):
        self._update_summary()

    def on_submit(self):
        self._create_service_tasks()

    def _update_summary(self):
        self.total_tasks = len(self.plan_lines)
        staff = sum(line.staff_count or 0 for line in self.plan_lines)
        self.total_staff_planned = staff

    def _create_service_tasks(self):
        for line in self.plan_lines:
            task = frappe.get_doc(
                {
                    "doctype": "Daily Service Task",
                    "daily_service_plan": self.name,
                    "plan_date": self.plan_date,
                    "client_site": self.client_site,
                    "service_type": line.service_type,
                    "shift_template": line.shift_template,
                    "assigned_employee": line.assigned_employee,
                    "status": "Pending",
                }
            )
            task.insert(ignore_permissions=True)
        frappe.msgprint(
            frappe._("{0} Daily Service Task(s) created.").format(len(self.plan_lines))
        )



