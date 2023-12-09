# Copyright (c) 2023, Quantum Bit Core and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from frappe.model.document import Document



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
def create_work_order(date):
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
			'item': item_name,
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