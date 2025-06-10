frappe.ui.form.on("Customer Training Log", {
    refresh(frm) {
        if (!frm.__intro_shown && frm.doc.customer && frm.doc.training_type && frm.doc.duration_days) {
            frm.set_intro(`
                <div style="
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    font-family: 'Courier New', monospace;
                    padding: 10px 15px;
                    border-radius: 8px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                    margin-top: 10px;
                    white-space: nowrap;
                    overflow-x: auto;
                ">
                    <span style="color: #8aff8a;">${frm.doc.customer}</span> ~ 
                    <span style="color: #f472b6;">${frm.doc.training_type}</span> →
                    Duration: <span style="color: #facc15;">${frm.doc.duration_days} Days</span> →
                    Start: <span style="color: #93c5fd;">${frm.doc.start_date}</span> →
                    End: <span style="color: #fda4af;">${frm.doc.end_date}</span> →
                    Feedback Due: <span style="color: #6ee7b7;">${frm.doc.feedback_due_date}</span>
                </div>
            `, false);
            frm.__intro_shown = true;
        }
    },
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

        // Reset intro flag on validation so it can re-show after save
        frm.__intro_shown = false;
        
    }
});
