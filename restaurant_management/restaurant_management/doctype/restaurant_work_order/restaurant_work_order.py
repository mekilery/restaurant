# Copyright (c) 2023, Quantum Bit Core and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	ceil,
	cint,
	comma_and,
	flt,
	get_link_to_form,
	getdate,
	now_datetime,
	nowdate,
)


class RestaurantWorkOrder(Document):
	def test():
		return

def sum_item_qty(json_list):
    result = {}
    for item in json_list:
        if item['item_name'] in result:
            result[item['item_name']]['item_qty'] += item['item_qty']
        else:
            result[item['item_name']] = item
    return list(result.values())

@frappe.whitelist()
def create_invoice_items(date):
	date_date=date
	# pos_invoice=frappe.get_doc("POS Invoice",pos_invoice_name)
	# last_restaurant_work_order=frappe.db.get_list('Restaurant Work Order',
    # filters={
	# 	'date': ['>', date]
    # }
	#  ,
    #  fields=['name', 'date'],
    #  order_by='date desc',
    # # start=10,
    # # page_length=20,
    # # as_list=True
	# )
	
	
	# items=pos_invoice.items

	last_restaurant_work_order=frappe.db.get_list('Restaurant Work Order',
    	fields=['max(date) as last_date'],
    	#group_by='status'
	)
	last_date=last_restaurant_work_order[0].last_date
	# if len(last_restaurant_work_order) > 0:
	if(last_date is not None):
		frappe.throw(_("There is Restaurant Work Order after this date {0} ").format(last_date))	


	
	pos_invoices=frappe.db.get_list('POS Invoice',
    filters={
		'posting_date': ['<=', date_date], #TODO Compaire time
		'pos_profile':"Restaurant POS Profile",
		'status':'Paid'
    }
	 ,
     fields=['name', 'posting_date'],
     order_by='posting_date asc',
    # start=10,
    # page_length=20,
    # as_list=True
	)
	item_list  = []
	for pos_invoice in pos_invoices:
	 
		pos_invoice_doc=frappe.get_doc("POS Invoice",pos_invoice.name)
		for pos_invoice_item in pos_invoice_doc.items:
			item_name=pos_invoice_item.item_name
			item_qty=pos_invoice_item.qty
			item_list.append({"item_name":item_name,"item_qty":item_qty,"status":"","bom":""})
			
	item_list=sum_item_qty(item_list)
 
	print (item_list)
	for item in item_list :
		bom=frappe.db.get_list('BOM',
		filters={
			'item': item['item_name'],
			'is_default':1
		}
		,
		# fields=['subject', 'date'],
		# order_by='date desc',
		# start=10,
		# page_length=20,
		# as_list=True
		)
		if len(bom) == 0:
			item['status']="BOM not exist"
		else:
			item['status']="pending"
			item['bom']=bom[0].name
	return {"items":item_list}
def create_work_order(item):
	item_doc=frappe.get_doc("Item",item.item)
	work_order = frappe.new_doc("Work Order")
	# if item_doc.get("warehouse"):
	# 	work_order.fg_warehouse = item_doc.get("warehouse")
	work_order.update(
		{
			"company": "alwatheq",
			"fg_warehouse": "Finished Goods - A",
			"production_item": item.item,
			"bom_no": item.bom,
			"qty": item.qty,
			#"stock_uom": "_Test UOM",
			"wip_warehouse": "All Warehouses - A",
			"skip_transfer": 1,
		}
	)
	work_order.insert()
	work_order.submit()

	from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry

	stock_entry = frappe.get_doc(make_stock_entry(work_order.name, "Manufacture", 1))
	stock_entry.insert()
		# from erpnext.manufacturing.doctype.work_order.work_order import OverProductionError
		# # from erpnext.manufacturing.doctype.work_order.work_order import make_work_order
		# if flt(item.get("qty")) <= 0:
		# 	return

		# item_doc=frappe.get_doc("Item",item.item_name)
		# wo = frappe.new_doc("Work Order")
		# wo.update(item_doc)
		# wo.planned_start_date = item_doc.get("planned_start_date") or item_doc.get("schedule_date")

		# if item_doc.get("warehouse"):
		# 	wo.fg_warehouse = item_doc.get("warehouse")

		# wo.set_work_order_operations()
		# wo.set_required_items()

		# try:
		# 	wo.flags.ignore_mandatory = True
		# 	wo.flags.ignore_validate = True
		# 	wo.insert()
		# 	return wo.name
		# except OverProductionError:
		# 	pass
@frappe.whitelist()
def prosses_work_order(work_order_name):
	 
	work_order=frappe.get_doc("Restaurant Work Order",work_order_name)
	 
 
	 
	item_list  = work_order.restaurant_work_order_item
 
	for item in item_list :
		if item.bom !='':
			if item.status=='pending':
				if item.work_order is None:
					work_order = create_work_order(item)
					if work_order:
						item.work_order=work_order
				if item.work_order is not None:
					work_order_doc=frappe.get_doc("Work Order",item.work_order)
					 
					
		# bom=frappe.db.get_list('BOM',
		# filters={
		# 	'item': item['item_name'],
		# 	'is_default':1
		# }
		# ,
		# # fields=['subject', 'date'],
		# # order_by='date desc',
		# # start=10,
		# # page_length=20,
		# # as_list=True
		# )
		# if len(bom) == 0:
		# 	item['status']="BOM not exist"
		# else:
		# 	item['status']="pending"
		# 	item['bom']=bom[0].name
	return {"items":item_list}

	# bom=frappe.db.get_list('BOM',
    # filters={
    #     'item': item_name,
	# 	'is_default':1
    # }
	# ,
    # # fields=['subject', 'date'],
    # # order_by='date desc',
    # # start=10,
    # # page_length=20,
    # # as_list=True
	# )
	# if len(bom) == 0:
	# 	frappe.throw(_("There is not BOM for this Item"))
	
	# bom=frappe.get_doc("BOM",bom_name)

	# frappe.throw(bom.name)
	# return {"bom":bom[0].name,"work_order":"xxx"}