import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
import calendar

class CustomerTrainingLog(Document):
    def validate(self):
        # Mandatory field validations
        if not self.customer:
            frappe.throw("Customer is mandatory.")
        if not self.training_type:
            frappe.throw("Training Type is mandatory.")
        if not self.start_date:
            frappe.throw("Start Date is mandatory.")
        if not self.end_date:
            frappe.throw("End Date is mandatory.")

        # Convert start_date and end_date from string to date
        if isinstance(self.start_date, str):
            self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        if isinstance(self.end_date, str):
            self.end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
            
        # Validate that start_date is not greater than end_date
        if self.start_date > self.end_date:
            frappe.throw("Start Date cannot be greater than End Date.")
            
        if self.start_date == self.end_date:
            frappe.throw("Start Date and End Date cannot be the same.")

        # Calculate duration (inclusive)
        self.duration_days = (self.end_date - self.start_date).days + 1

        # Set feedback_due_date based on training_type
        days_map = {
            "Basic": 7,
            "Advanced": 14,
            "Special": 21
        }
        self.feedback_due_date = self.end_date + timedelta(days=days_map.get(self.training_type, 7))

        # Prevent duplicate entries for same month
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
