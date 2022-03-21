# Copyright (c) 2013, Ebkar Technology. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)


	return columns, data

def get_columns(filters):
	return [
		{
			"fieldname": "item",
			"label": _("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"width": "150"
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Data",
			"width": "120"
		},
		{
			"fieldname": "item_group",
			"label": _("Item Group"),
			"fieldtype": "Data",
			"width": "120"
		},
		{
			"fieldname": "brand",
			"label": _("Brand"),
			"fieldtype": "Data",
			"width": "120"
		},
		{
			"fieldname": "description",
			"label": _("Description"),
			"fieldtype": "Data",
			"width": "140"
		},
		{
			"fieldname": "warehouse",
			"label": _("Warehouse"),
			"fieldtype": "Data",
			"width": "180"
		},
		{
			"fieldname": "actual_qty",
			"label": _("Balance Qty"),
			"fieldtype": "Data",
			"width": "110"
		},
		{
			"fieldname": "storage_locations",
			"label": _("Storage Locations"),
			"fieldtype": "Data",
			"width": "150"
		},
	]

def get_data(filters):
	data = []
	sql_filter = ""

	if(filters.get("item")):
		sql_filter += f"""where a.item_code = "{filters.get("item")}" """

	if(filters.get("warehouse")):
		sql_filter += f"""where c.warehouse = "{filters.get("warehouse")}" """

	if(filters.get("item") and filters.get("warehouse")):
		sql_filter = ""
		sql_filter += f"""where a.item_code = "{filters.get("item")}" and c.warehouse = "{filters.get("warehouse")}" """

	sql_list = frappe.db.sql(f"""
		select a.*, c.warehouse, c.actual_qty
		from (
			select a.item_code, a.item_name, a.item_group, a.brand, a.description,
			group_concat(b.storage_location_in_warehouse order by b.storage_location_in_warehouse asc separator ', ') 
			as joined_locations

			from `tabItem` as a left outer join `tabItem Storage Location in Warehouse` as b
			on a.item_code = b.parent
			
			group by a.item_code

		) as a left outer join `tabBin` as c
		on a.item_code = c.item_code
		{sql_filter}

	""", as_dict=True)

	for item in sql_list:
		data.append(
			{
				"item": item.item_code,
				"item_name": item.item_name,
				"item_group": item.item_group,
				"brand": item.brand,
				"description": item.description,
				"warehouse": item.warehouse,
				"actual_qty": item.actual_qty,
				"storage_locations": item.joined_locations
			}
		)

	return data