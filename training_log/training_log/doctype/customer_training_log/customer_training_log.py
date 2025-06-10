import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
import calendar

class CustomerTrainingLog(Document):
    def validate(self):
        self._validate_mandatory_fields()
        self._convert_dates()
        self._validate_dates()
        self._calculate_duration()
        self._set_feedback_due_date()
        self._check_for_duplicates()

    def _validate_mandatory_fields(self):
        for field in ["customer", "training_type", "start_date", "end_date"]:
            if not getattr(self, field):
                frappe.throw(f"{field.replace('_', ' ').title()} is mandatory.")

    def _convert_dates(self):
        if isinstance(self.start_date, str):
            self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        if isinstance(self.end_date, str):
            self.end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()

    def _validate_dates(self):
        if self.start_date > self.end_date:
            frappe.throw("Start Date cannot be greater than End Date.")
        if self.start_date == self.end_date:
            frappe.throw("Start Date and End Date cannot be the same.")

    def _calculate_duration(self):
        self.duration_days = (self.end_date - self.start_date).days + 1

    def _set_feedback_due_date(self):
        feedback_days = {"Basic": 7, "Advanced": 14, "Special": 21}
        self.feedback_due_date = self.end_date + timedelta(days=feedback_days.get(self.training_type, 7))

    def _check_for_duplicates(self):
        month_start = self.start_date.replace(day=1)
        last_day = calendar.monthrange(self.start_date.year, self.start_date.month)[1]
        month_end = self.start_date.replace(day=last_day)

        exists = frappe.db.exists(
            "Customer Training Log",
            {
                "customer": self.customer,
                "training_type": self.training_type,
                "start_date": ["between", [month_start, month_end]],
                "name": ["!=", self.name]
            }
        )
        if exists:
            frappe.throw("Duplicate training log found for this customer and training type in the same month.")
