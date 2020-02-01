

class Product():
    def __init__(self, code, name, length, width, height, standard_qty, FP_qty, despatchable_flag, haz_class = "00"):
        self.code = code
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.haz_class = haz_class
        self.volume = length * width * height
        self.standard_qty = standard_qty
        self.FP_qty = FP_qty
        self.despatchable_flag = despatchable_flag