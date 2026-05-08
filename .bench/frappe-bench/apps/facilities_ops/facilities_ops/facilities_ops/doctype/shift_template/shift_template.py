import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta


class ShiftTemplate(Document):
    def validate(self):
        self._calculate_duration()

    def _calculate_duration(self):
        if self.start_time and self.end_time:
            fmt = "%H:%M:%S"
            start = datetime.strptime(str(self.start_time), fmt)
            end = datetime.strptime(str(self.end_time), fmt)
            if end < start:
                end += timedelta(days=1)
                self.is_overnight = 1
            else:
                self.is_overnight = 0
            delta = end - start
            self.duration_hours = round(delta.seconds / 3600, 2)
