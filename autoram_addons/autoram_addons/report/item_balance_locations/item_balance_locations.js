// Copyright (c) 2016, Ebkar Technology. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Balance Locations"] = {
	"filters": [
		{
			fieldname: "item",
			label: frappe._("Item"),
			fieldtype: "Link",
			reqd: 0,
			options: "Item"
		},
		{
			fieldname: "warehouse",
			label: frappe._("Warehouse"),
			fieldtype: "Link",
			reqd: 0,
			options: "Warehouse"
		}

	],
	after_datatable_render: function(datatable_obj) {
		// rows = datatable_obj.getRows();
	},
};
