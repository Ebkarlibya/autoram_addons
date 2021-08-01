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
			"fieldname": "technician_name",
			"label": _("Technician Name"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": "176"
		},
		{
			"fieldname": "invoice_name",
			"label": _("Invoice"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": "144"
		},
		{
			"fieldname": "invoice_status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": "70"
		},
		{
			"fieldname": "invoice_currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"width": "80"
		},
		{
			"fieldname": "item_name",
			"label": _("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"width": "180"
		},
		{
			"fieldname": "item_group",
			"label": _("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
			"width": "90"
		},
		{
			"fieldname": "item_uom",
			"label": _("UOM"),
			"fieldtype": "Link",
			"options": "UOM",
			"width": "50"
		},
				{
			"fieldname": "item_qty",
			"label": _("Quantity"),
			"fieldtype": "Data",
			"width": "73"
		},
		{
			"fieldname": "amount",
			"label": _("Amount"),
			"fieldtype": "Currency",
			"width": "110"
		},
		{
			"fieldname": "commission_rate",
			"label": _("Commission Rate"),
			"fieldtype": "Float",
			"width": "120"
		},
		{
			"fieldname": "commission",
			"label": _("Commission Amount"),
			"fieldtype": "Currency",
			"width": "145"
		}

	]

def get_data(filters):
	tmp_row = {}
	data = []
	idx = 0
	total_commission = 0
	total_amount = 0
	filters_dict = {"docstatus": "1"}

	si_orm = None

	if(filters.get("from_date")):
		filters_dict["posting_date"] = [">=", filters.get("from_date"), "<=", filters.get("to_date")]

	if(filters.get("sales_invoice")):
		filters_dict["name"] = filters.get("sales_invoice")

	if(filters.get("currency")):
		filters_dict["currency"] = filters.get("currency")

	si_list = frappe.get_all("Sales Invoice", fields=["name", "currency"], filters=filters_dict)
	
	while(idx < len(si_list)):
		# get si orm for each si list item
		si_orm = frappe.get_doc("Sales Invoice", si_list[idx].name)

		for item in si_orm.items:
			if item.technician != filters.technician \
				or (filters.item and filters.item != item.item_code) \
				or (filters.item_group and filters.item_group != item.item_group):
				continue
			tmp_row = {
				"technician_name": item.technician_name,
				"invoice_name": si_orm.name,
				"invoice_status": si_orm.status,
				"invoice_currency": si_list[idx].currency,
				"item_name": item.item_name,
				"item_group": item.item_group,
				"item_uom": item.uom,
				"item_qty": frappe.utils.flt(item.qty),
				"amount": item.amount,
				"commission": frappe.format_value(item.technician_commission_amount, "Currency"),
				"commission_rate": frappe.utils.flt(item.technician_commission_rate, 2)
			}
			data.append(tmp_row)
			total_amount += item.amount
			total_commission += item.technician_commission_amount
		
		idx+=1

	# calculate totals
	if (len(data) >= 1):
		totals = {
				"technician_name": "Total",
				"amount": frappe.format_value(total_amount, "Currency"),
				"commission": frappe.format_value(total_commission, "Currency"),
		}
		data.append(totals)
	return data