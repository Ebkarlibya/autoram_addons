// Copyright (c) 2016, Ebkar Technology. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Technician Commission"] = {
	"filters": [
		{
			fieldname: "technician",
			label: "Technician",
			fieldtype: "Link",
			reqd: 1,
			options: "Employee",
			get_query: function () {
				return {
					"filters": {
						"technician_gets_a_commission": 1
					}
				}
			}
		},
		{
			fieldname:"from_date",
			reqd: 1,
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname:"to_date",
			reqd: 1,
			default: frappe.datetime.get_today(),
			label: __("To Date"),
			fieldtype: "Date",
		},
		{
			fieldname:"sales_invoice",
			label: __("Sales Invoice"),
			fieldtype: "Link",
			options: "Sales Invoice",
			get_query: function () {
				return {
					filters: {
						"docstatus": "1"
					}
				}
			}
		},
		{
			fieldname:"item",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item"
		},
		{
			fieldname:"item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group"
		},
		{
			fieldname:"currency",
			default: frappe.defaults.get_default("currency"),
			label: __("Currency"),
			fieldtype: "Link",
			options: "Currency"
		},
		{
			fieldname:"si_paid",
			default: true,
			label: __("SI Paid"),
			fieldtype: "Check"
		},
		{
			fieldname:"si_unpaid",
			default: false,
			label: __("SI Unpaid"),
			fieldtype: "Check"
		},
		{
			fieldname:"si_overdue",
			default: false,
			label: __("SI Overdue"),
			fieldtype: "Check"
		},
		{
			fieldname:"si_return",
			default: false,
			label: __("SI Return"),
			fieldtype: "Check"
		}
	],
	after_datatable_render: function(datatable_obj) {
		rows = datatable_obj.getRows();
		if(rows && rows.length > 0 ) {
			last_row = rows[rows.length -1]
			console.log(last_row)
			last_row[1].content = "<b>Total:</b>";
			last_row[9].content = "<b>" + last_row[9].content + "</b>";
			last_row[11].content = "<b>" + last_row[11].content + "</b>";
			datatable_obj.refreshRow(last_row);
		}
	},
};
