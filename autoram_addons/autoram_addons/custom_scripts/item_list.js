frappe.listview_settings['Item'] = {
	add_fields: ["item_name", "stock_uom", "item_group", "image", "variant_of",
		"has_variants", "end_of_life", "disabled"],
	// filters: [["disabled", "=", "0"]],
    onload: function(lv, t){
        var cbtn = document.createElement("button");
        cbtn.className = "btn btn-default btn-xs filter-add-button text-muted d-clear-filters";
        cbtn.innerHTML = frappe._("Add Vehicle Filters");
        cbtn.style.marginBottom = "10px";
        // cbtn.style.float = "right";

        cbtn.addEventListener("click", function(e) {

            let d = new frappe.ui.Dialog({
            title: frappe._('Vehicles Filter'),
            fields: [
                {
                    label: frappe._('Vehicle Make'),
                    fieldname: 'vehicle_manufacturers',
                    fieldtype: 'Link',
                    options: "Vehicle Manufacturers",                },
                {
                    
                    fieldname: 'column_break0',
                    fieldtype: 'Column Break',
                },
                {
                    label: frappe._('Vehicle Model'),
                    fieldname: 'vehicle_model',
                    fieldtype: 'Link',
                    options: "Vehicles Model"
                },
                {
                    
                    fieldname: 'column_break1',
                    fieldtype: 'Column Break',
                },
                {
                    label: frappe._('Model Year'),
                    fieldname: 'year_model_v',
                    fieldtype: 'Data'                },
                {
                    
                    fieldname: 'column_break2',
                    fieldtype: 'Column Break',
                },
                {
                    label: frappe._('Engine'),
                    fieldname: 'vehicle_engine',
                    fieldtype: 'Link',
                    options: "Engine"
                },
            ],
            primary_action_label: frappe._('Set Filters'),
            primary_action(values) {
                cur_list.filter_area.filter_list.add_filter("Compatible with", "vehicle_manufacturers", "=", values.vehicle_manufacturers);
                cur_list.filter_area.filter_list.add_filter("Compatible with", "vehicles_model", "=", values.vehicle_model);
                cur_list.filter_area.filter_list.add_filter("Compatible with", "year_model_v", "like", values.year_model_v);
                cur_list.filter_area.filter_list.add_filter("Compatible with", "engine", "=", values.vehicle_engine);

                d.hide();
            }
            });
        d.show();
    });
        document.querySelector(".active-tag-filters").appendChild(cbtn)
    },
	get_indicator: function(doc) {
		if (doc.disabled) {
			return [__("Disabled"), "grey", "disabled,=,Yes"];
		} else if (doc.end_of_life && doc.end_of_life < frappe.datetime.get_today()) {
			return [__("Expired"), "grey", "end_of_life,<,Today"];
		} else if (doc.has_variants) {
			return [__("Template"), "orange", "has_variants,=,Yes"];
		} else if (doc.variant_of) {
			return [__("Variant"), "green", "variant_of,=," + doc.variant_of];
		}
	},

	reports: [
		{
			name: 'Stock Summary',
			report_type: 'Page',
			route: 'stock-balance'
		},
		{
			name: 'Stock Ledger',
			report_type: 'Script Report'
		},
		{
			name: 'Stock Balance',
			report_type: 'Script Report'
		},
		{
			name: 'Stock Projected Qty',
			report_type: 'Script Report'
		}

	]
};

frappe.help.youtube_id["Item"] = "qXaEwld4_Ps";
