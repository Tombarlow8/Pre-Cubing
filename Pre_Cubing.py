import Box_Classes as Bc
import Product_Classes as Pc
import csv
import pandas


def load_products_from_csv(file_name):
	data_frame = pandas.DataFrame(pandas.read_csv(file_name))
	for row in data_frame.iterrows():
		# [code, name, length, width, height, standard_qty, FP_qty, despatchable_flag,  haz_class]
		my_product_array = [str(row[1][0]), str(row[1][1]), row[1][2], row[1][3], row[1][4], row[1][5], row[1][6], str(row[1][7]), str(row[1][8])]
		create_products_from_csv_QTY(row, my_product_array)

def create_products_from_csv_QTY(row, my_product_array): 
	product_quantity = row[1][9]
	product_standard_qty = row[1][5]
	product_full_pallet_qty = row[1][6]
	my_product = Pc.Product(*my_product_array)
	
	number_of_FP = (product_quantity - (product_quantity % product_full_pallet_qty)) // product_full_pallet_qty
	
	for i in range(product_quantity % product_full_pallet_qty % product_standard_qty):
		our_products.append(my_product)
	# TODO: refactor into own method 
	for i in range(number_of_FP):
		Full_pallet = Bc.FP(my_product.code)
		for i in range(0, product_full_pallet_qty):
			Full_pallet.FP_pack(my_product)
		full_pallet_group.append(Full_pallet)

	if product_quantity % product_full_pallet_qty == 0:
		number_of_standards = 0
	else:
		number_of_standards = ((product_quantity - (number_of_FP * product_full_pallet_qty)) - (product_quantity % product_full_pallet_qty % product_standard_qty)) // product_standard_qty
	# TODO: refactor into own method 
	for i in range(number_of_standards):
		standard_box = Bc.STD_box(my_product.code)
		for i in range(0, product_standard_qty):
			standard_box.std_pack(my_product)
		standard_group.append(standard_box)


def pack_and_clear(current_group, new_group, groups_of_products):
    new_group.pack(current_group)
    groups_of_products.append(new_group)
    current_group.clear()


# TODO: reference some sort of table 
def check_hazards_in_group(aproduct, group):
    check_bool = False
    if len(group) != 0:
        for product in group:
            if product.haz_class == "D5" and aproduct.haz_class == "C7":
                check_bool = True
                break
            elif product.haz_class == "C7" and aproduct.haz_class == "D5":
                check_bool = True
                break
            elif product.haz_class == "00":
                continue
    else:
        check_bool = False

    return check_bool
	
   
# TODO: condition not being met which exludes products from being added to a group     
# add products into groups upto a limit
def Create_box_group(count, current_group, groups_of_products, our_products, product, temp_vol):
	if check_hazards_in_group(product, current_group) == False:
	    # print(f"count {count} lengh: {len(our_products)}")
	    temp_vol += product.volume
	    # print(f"temp vol: {temp_vol} ")
	    if temp_vol < box4vol and len(our_products) != count:
	        current_group.append(product)
	    elif temp_vol > box4vol: #  and count != len(our_products):
	        temp_vol -= temp_vol
	        new_group = Bc.box_group()
	        pack_and_clear(current_group, new_group, groups_of_products)
	        # there will be a stray product which will need adding # DONE i think
	        our_products.append(product)
	    elif temp_vol < box4vol  and len(our_products) != count:
	        temp_vol -= temp_vol
	        new_group = Bc.box_group()
	        pack_and_clear(current_group, new_group, groups_of_products)
	    elif temp_vol < box4vol  and len(our_products) == count:
	        temp_vol -= temp_vol
	        new_group = Bc.box_group()
	        current_group.append(product)
	        pack_and_clear(current_group, new_group, groups_of_products)
	elif check_hazards_in_group(product, current_group) and temp_vol < box4vol  and len(our_products) == count:
	    temp_vol -= temp_vol
	    new_group = Bc.box_group()
	    pack_and_clear(current_group, new_group, groups_of_products)
	else:
	    somewhere_else.append(product)
	return temp_vol


def group_products_box_groups(our_products):
    groups_of_products = []
    current_group = []  
    temp_vol = 0
    for count, product in enumerate(our_products, start=1):  
            temp_vol = Create_box_group(count, current_group, groups_of_products, our_products, product, temp_vol)
    return groups_of_products


# pack the grups into boxes according to size
def pack_groups_into_into_boxes(groups_of_products):
    group_vol = 0
    boxes_in_delivery = []
    for group in groups_of_products:
        for product in group.contents:
            group_vol += product.volume  
        if group_vol < box2vol:
            new_box = Bc.P2_box()
            group_vol -= group_vol
            new_box.pack(group.contents)
        elif group_vol > box2vol and group_vol < box3vol:
            new_box = Bc.P3_box()
            group_vol -= group_vol
            new_box.pack(group.contents)
        elif group_vol > box3vol:
            new_box = Bc.P4_box()
            group_vol -= group_vol
            new_box.pack(group.contents)
        boxes_in_delivery.append(new_box)

    return boxes_in_delivery


def pre_cubing_results():

	product_count = 0

	for box in my_boxes:
		for products in box.contents:
			product_count += 1
		print(f"box_type = {box.box_type}, box_vol = {box.get_contents_vol()}")
		print(box.show_haz_list())
		
	# This is a temp funtion for debugging
	# for box in my_boxes2:
	# 	for products in box.contents:
	# 		product_count += 1
	# 	print(f"box_type = {box.box_type}, box_vol = {box.get_contents_vol()}")
	# 	print(box.show_haz_list())


	for standard in standard_group:
		print(f"product = {standard.product}, box_type = {standard.box_type}")

	for full_pallet in full_pallet_group:
		print(f"product = {full_pallet.product}, box_type = {full_pallet.box_type}")

	print(f"product count = {product_count}")

	if len(somewhere_else)  > 0:
		print("ERROR: There is an exception for the ore-cubing statements")


if __name__ == "__main__":

	full_pallet_group = []
	standard_group = []
	our_products = []
	# This is a temp list for debugging
	somewhere_else = []
	product_csv_file = r"C:\Users\TomBa\VSCode Files\Python\Python_Workbench\Warehouse_programming\WM_products.csv"
	box2vol = Bc.P2_box().volume
	box3vol = Bc.P3_box().volume
	box4vol = Bc.P4_box().volume

	# get the product master data form a csv file and then create the products as 'Product' Objects
	load_products_from_csv(product_csv_file)
	
	my_groups = group_products_box_groups(our_products)
	my_boxes = pack_groups_into_into_boxes(my_groups)

	pre_cubing_results()
	



