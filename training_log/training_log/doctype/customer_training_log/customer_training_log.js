frappe.ui.form.on("Customer Training Log", {
    validate(frm) {
        if (!frm.doc.customer) {
            frappe.msgprint("Customer is mandatory");
            frappe.validated = false;
            return;
        }
        if (!frm.doc.training_type) {
            frappe.msgprint("Please select a valid Training Type");
            frappe.validated = false;
            return;
        }
        if (!frm.doc.start_date) {
            frappe.msgprint("Start Date is mandatory");
            frappe.validated = false;
            return;
        }
        if (!frm.doc.end_date) {
            frappe.msgprint("End Date is mandatory");
            frappe.validated = false;
            return;
        }
        
    }
});
