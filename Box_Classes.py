import Product_Classes as Pc


class box():
    def __init__(self, box_type, length, width, height):
        self.box_type = box_type
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height
        self.contents = []
        self.fill_volume = 0
        self.haz_list = []

    def show_haz_list(self):
        for product in self.contents:
            if self.haz_list.__contains__(product.haz_class) == False:
                self.haz_list.append(product.haz_class)
        return self.haz_list

    def get_contents_vol(self):
        contents_vol = 0
        for product in self.contents:
            contents_vol += product.volume
        return contents_vol

    def pack(self, products):
        for product in products:
            if product.volume + self.fill_volume < self.volume:
                self.fill_volume += product.volume
                self.contents.append(product)
            else:
                # orphan product for now
                pass


    def show_contents(self):
        for product in self.contents:
            print(f"Product: {product.name}")
        print(self.fill_volume)


class P2_box(box):
    def __init__(self,box_type = "P2", length = 200, width = 140, height = 140):
        super().__init__(box_type, length, width, height)


class P3_box(box):
    def __init__(self,box_type = "P3", length = 300, width = 200, height = 200):
        super().__init__(box_type,length, width, height)


class P4_box(box):
    def __init__(self,box_type = "P4", length = 300, width = 300, height = 300):
        super().__init__(box_type,length, width, height)

class STD_box(box):
    def __init__(self, product = "", box_type = "STD", length = 0 , width = 0, height = 0):
        super().__init__(box_type, length, width, height)
        self.product = product

    def std_pack(self, product):
        self.contents.append(product)

class FP(box):
    def __init__(self, product = "", box_type = "FP", length = 0 , width = 0, height = 0):
        super().__init__(box_type, length, width, height)
        self.product = product

    def FP_pack(self, product):
        self.contents.append(product)

class box_group():
    def __init__(self):
        self.contents = []
        self.fill_volume = 0       

    def pack(self, group_contents):
        for group_content in group_contents:
                self.contents.append(group_content)

    def show_contents(self):
        for c in self.contents:
            print(c)