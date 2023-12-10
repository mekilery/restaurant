// Copyright (c) 2023, Quantum Bit Core and contributors
// For license information, please see license.txt

frappe.ui.form.on('Restaurant Work Order', {
	refresh: function (frm) {
		if (frm.doc.status != 'aaaa') {
			frm.add_custom_button(__('Update BOM'), function () {

				frappe.call({
					method: `restaurant_management.restaurant_management.doctype.restaurant_work_order.restaurant_work_order.update_bom`,
					args: {
						 
						date: frm.doc.date
					},
					callback: function (r) {
						// frm.set_value("bom", r.message.bom)

					}
				});

			}, __("Actions"));
		}
		if (frm.doc.status != 'aaaa') {
			frm.add_custom_button(__('Start Prosess'), function () {

				frappe.call({
					method: `restaurant_management.restaurant_management.doctype.restaurant_work_order.restaurant_work_order.prosses_work_order`,
					args: {
						 
						work_order_name: frm.doc.name
					},
					callback: function (r) {
						// frm.set_value("bom", r.message.bom)

					}
				});

			}, __("Actions"));
		}
	},
	// item: function (frm) {
	// 	if (frm.doc.datework_order_name != undefined) {
	// 		frm.set_value("bom", undefined)
	// 		frappe.call({
	// 			method: `restaurant_management.restaurant_management.doctype.restaurant_work_order.restaurant_work_order.create_work_order`,
	// 			args: {
	// 				item_name: frm.doc.item,
	// 				date: frm.doc.date
	// 			},
	// 			callback: function (r) {
	// 				frm.set_value("bom", r.message.bom)
	// 				frm.set_value("qty", 10)
	// 			}
	// 		});
	// 	}

	// },
	date: function (frm) {

		let d1 = frm.doc.date
		let date1 = new Date(d1).getTime();
		var date = new Date();
		let currentDate = date.getTime();


		var d2 =
			("00" + (date.getMonth() + 1)).slice(-2) + "-" +
			("00" + date.getDate()).slice(-2) + "-" +
			date.getFullYear() + " " +
			("00" + date.getUTCHours()).slice(-2) + ":" +
			("00" + date.getUTCMinutes()).slice(-2) + ":" +
			("00" + date.getUTCSeconds()).slice(-2);
		

		if (date1 < currentDate) {
			console.log(`${d1} is less than ${d2}`);
		} else if (date1 > currentDate) {
			console.log(`${d1} is greater than ${d2}`);
			frm.set_value("date", d2)
		} else {
			console.log(`Both dates are equal`);
		}

		frappe.call({
			method: `restaurant_management.restaurant_management.doctype.restaurant_work_order.restaurant_work_order.create_invoice_items`,
			args: {
				date: frm.doc.date
			},
			callback: function (r) {
				// frm.set_value("bom", r.message.bom)
				frm.set_value("restaurant_work_order_item" ,[]);
                frm.refresh_field('restaurant_work_order_item');
                $.each(r.message.items,function(_i,e){
                     console.log("helper->",e.item_name)
                     let item=frm.add_child("restaurant_work_order_item");
                     item.item=e.item_name;
                     item.qty=e.item_qty; 
					 item.bom=e.bom; 
					 item.status=e.status;
                    //  if(e[2]!=null)
                    //     item.start_time=e[2];
                    //  else 
                    //     item.start_time="08:00:00";
                    // if(e[3]!=null)
                    //     item.end_time=e[3];
                    // else
                    //     item.end_time="18:00:00";
                })
				frm.refresh_field('restaurant_work_order_item');
			}
		});



	}


});
