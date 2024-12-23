import frappe

def before_uninstall():
    # Step 1: Delete custom fields in 'Lead' that might reference the non-existing 'District' or 'Municipality' doctype
    fields_to_delete = [
        "district", "municipality", "ward", "select_area_type", "ropani",
        "aana", "paisa", "daam", "bigha", "kattha", "dhur", 
        "square_feet", "square_meter"
    ]

    for field in fields_to_delete:
        try:
            # Delete the custom field from 'Lead' doctype
            frappe.db.sql(f"DELETE FROM `tabCustom Field` WHERE fieldname = '{field}' AND parent = 'Lead'")
            frappe.db.commit()  # Commit changes to the database
            frappe.msgprint(f"Custom field '{field}' removed from 'Lead'.")
        except Exception as e:
            frappe.log_error(f"Error deleting custom field '{field}': {str(e)}")

    # Step 2: Delete custom doctypes 'district' and 'municipality'
    try:
        # Ensure we delete the 'district' and 'municipality' doctypes if they exist
        if frappe.db.exists("DocType", "district"):
            frappe.delete_doc("DocType", "district", force=True)
            frappe.msgprint("DocType 'district' removed.")
        if frappe.db.exists("DocType", "municipality"):
            frappe.delete_doc("DocType", "municipality", force=True)
            frappe.msgprint("DocType 'municipality' removed.")
    except Exception as e:
        frappe.log_error(f"Error deleting doctypes: {str(e)}")

    # Step 3: Clean up any other related data created by ajira_mods
    try:
        # Clean up custom fields, property setters, and other app-specific records
        frappe.db.sql("DELETE FROM `tabCustom Field` WHERE app_name = 'ajira_mods'")
        frappe.db.sql("DELETE FROM `tabProperty Setter` WHERE app_name = 'ajira_mods'")
        frappe.db.sql("DELETE FROM `tabCustom Script` WHERE app_name = 'ajira_mods'")
        frappe.db.sql("DELETE FROM `tabCustom DocPerm` WHERE app_name = 'ajira_mods'")
        frappe.db.commit()  # Commit the changes to remove related data
        frappe.msgprint("Cleaned up related data from ajira_mods.")
    except Exception as e:
        frappe.log_error(f"Error cleaning up related data: {str(e)}")

    # Optional: If you have other app-specific records in additional tables, you can delete them here.
    # Example:
    # frappe.db.sql("DELETE FROM `tabSomeOtherTable` WHERE app_name = 'ajira_mods'")
