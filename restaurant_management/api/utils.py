import frappe

def get_item_groups(pos_profile):
	item_groups = []
	pos_profile = frappe.get_cached_doc("POS Profile", pos_profile)

	if pos_profile.get("item_groups"):
		# Get items based on the item groups defined in the POS profile
		for data in pos_profile.get("item_groups"):
			item_groups.extend(
				["%s" % frappe.db.escape(d.name) for d in get_child_nodes("Item Group", data.item_group)]
			)

	return list(set(item_groups))

def get_child_nodes(group_type, root):
	lft, rgt = frappe.db.get_value(group_type, root, ["lft", "rgt"])
	return frappe.db.sql(
		""" Select name, lft, rgt from `tab{tab}` where
			lft >= {lft} and rgt <= {rgt} order by lft""".format(
			tab=group_type, lft=lft, rgt=rgt
		),
		as_dict=1,
	)

@frappe.whitelist()
def food_group(pos_profile):
  item_groups = get_item_groups(pos_profile)
  cond = "name in (%s)" % (", ".join(["%s"] * len(item_groups)))
  cond = cond % tuple(item_groups)
  query = f"select distinct name from `tabItem Group` where {cond}"
  result =  frappe.db.sql(query)
  final_output = []
  for item in result:
    final_output.append(item[0])
  return final_output


