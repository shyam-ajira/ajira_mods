import frappe

def before_uninstall():
    # List of fields to delete from 'tabLead'
    fields_to_delete = [
        "district", "municipality", "ward", "select_area_type", "ropani",
        "aana", "paisa", "daam", "bigha", "kattha", "dhur", 
        "square_feet", "square_meter"
    ]
    
    # Delete custom fields from 'tabLead'
    for field in fields_to_delete:
        try:
            frappe.db.sql(f"DELETE FROM `tabCustom Field` WHERE fieldname = '{field}' AND parent = 'Lead'")
        except Exception as e:
            frappe.log_error(f"Error deleting custom field {field}: {str(e)}")
    
    # Delete the custom doctypes 'district' and 'municipality'
    try:
        frappe.delete_doc("DocType", "district", force=True)
        frappe.delete_doc("DocType", "municipality", force=True)
    except Exception as e:
        frappe.log_error(f"Error deleting doctypes: {str(e)}")

    # Optional: Clean up related data (e.g., Property Setters, Custom Scripts)
    try:
        frappe.db.sql("DELETE FROM `tabCustom Field` WHERE app_name = 'ajira_mods'")
        frappe.db.sql("DELETE FROM `tabProperty Setter` WHERE app_name = 'ajira_mods'")
        frappe.db.sql("DELETE FROM `tabCustom Script` WHERE app_name = 'ajira_mods'")
        frappe.db.sql("DELETE FROM `tabCustom DocPerm` WHERE app_name = 'ajira_mods'")
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(f"Error cleaning up related data: {str(e)}")
