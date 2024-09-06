import numpy as np
from part import *
from tqdm import tqdm

class WareHouse:
    def __init__(self, product_info) -> None:
        self.product_info = product_info
        self.warehouse = self.construct_warehouse()
    
    def construct_warehouse(self):
        warehouse = {}
        for product in self.product_info.keys():
            warehouse[product] = []
        return warehouse
    
    def add_inventory(self, item: Part):
        self.warehouse[item.get_name()].append(item)
    
    def get_item(self, name, index):
        return self.warehouse[name][index]
    
    def get_batch(self, name):
        return self.warehouse[name]

    def get_fail_rate(self, name):
        return self.product_info[name]['fail_rate']

    def get_unit_cost(self, name):
        return self.product_info[name]['unit_cost']
    
    def get_assemble_cost(self, name):
        return self.product_info[name]['assemble_cost']
    
    def get_check_cost(self, name):
        return self.product_info[name]['check_cost']
    
    def get_disassemble_cost(self, name):
        return self.product_info[name]['disassemble_cost']
    
    def get_available_number(self, material_list: list):
        number = []
        for material in material_list:
            number.append(len(self.warehouse[material]))
        return min(number)
    
    def get_market_value(self, name):
        return self.product_info[name]['market_value']
    
    def get_exchange_cost(self, name):
        return self.product_info[name]['exchange_cost']
    
    def remove_parts_batch(self, name, number: int):
        self.warehouse[name][:] = self.warehouse[name][number:]
    
    def remove_parts_each(self, item: Part):
        name = item.get_name()
        self.warehouse[name].remove(item)

class Factory:
    def __init__(self, warehouse: WareHouse) -> None:
        self.warehouse = warehouse
        self.cost = 0
        self.income = 0
        self.exchange_product = []
        self.final_customer_flag = 0
        self.final_qualified_product = 0
    
    def buy_parts(self, part_name, number):
        for _ in range(number):
            if np.random.rand() > self.warehouse.get_fail_rate(part_name):
                item = Part(part_name, 1)
            else:
                item = Part(part_name, 0)
            self.warehouse.add_inventory(item)
        self.cost += self.warehouse.get_unit_cost(part_name) * number
    
    def assemble(self, material_list, target_product):
        # 获取能够装配的数量
        available_number = self.warehouse.get_available_number(material_list)
        # 根据最少的那种材料的数量生产目标产品
        for i in range(available_number):
            used_material = []
            for material in material_list:
                used_material.append(self.warehouse.get_item(material, i))

            for material in material_list:
                if not self.warehouse.get_item(material, i).is_qualified():
                    item = Part(target_product, 0, used_material)
                    self.warehouse.add_inventory(item)

            if np.random.rand() > self.warehouse.get_fail_rate(target_product):
                item = Part(target_product, 1, used_material)
                self.warehouse.add_inventory(item)
            else:
                item = Part(target_product, 0, used_material)
                self.warehouse.add_inventory(item)

        # 计算装配成本
        self.cost += self.warehouse.get_assemble_cost(target_product) * available_number

        # 将已经使用的零件从库存去除
        for material in material_list:
            self.warehouse.remove_parts_batch(material, available_number)



    def check_each(self, item, disassemble=False):
        if not disassemble:
            if not item.is_qualified():
                self.warehouse.remove_parts_each(item)
        else:
            if not item.is_qualified():
                self.disassemble(item)
        
        self.cost += self.warehouse.get_check_cost(item.get_name())
    
    def check_batch(self, name, disassemble=False):
        for item in self.warehouse.get_batch(name):
            self.check_each(item, disassemble=disassemble)

    def disassemble(self, item):
        materials = item.get_material()
        self.cost += self.warehouse.get_disassemble_cost(item.get_name())
        self.warehouse.remove_parts_each(item)
        for material in materials:
            self.warehouse.add_inventory(material)
    
    def disassemble_batch(self, name):
        for item in self.warehouse.get_batch(name):
            self.disassemble(item)

    # def disassemble_exchange_product(self):
    #     for item in self.exchange_product:
    #         self.disassemble(item)
    
    def sell(self, name):
        final_product = self.warehouse.get_batch(name)

        # 记录第一次售出的成品数量，之后至少要满足有这么多的成品
        if self.final_customer_flag == 0:
            self.final_customer = len(final_product)
            self.final_customer_flag = 1

        for product in final_product:
            if product.is_qualified:
                self.warehouse.remove_parts_each(product)
                self.final_qualified_product += 1
                self.income += self.warehouse.get_market_value(name)
            else:
                self.cost += self.warehouse.get_exchange_cost(name)
    
    def drop_product(self, name):
        """仅仅在最终售卖结束的时候用于丢弃不拆解的产品"""
        for item in self.warehouse.get_batch(name):
            self.warehouse.remove_parts_each(item)
        
    # def exchange(self, name):
    #     final_product = self.warehouse.get_batch(name)
    #     self.exchange_product = []
    #     for product in final_product:
    #         if not product.is_qualified():
    #             self.cost += self.warehouse.get_exchange_cost(name)
    #             self.exchange_product.append(product)
    #         else:
    #             self.warehouse.remove_parts_each(product)
    #     self.final_qualified_product -= len(self.exchange_product)
    
    def stop_manu(self, parts_name_list):
        if self.warehouse.get_available_number(parts_name_list) == 0:
            return True
        return False
    
    def after_sale_service(self, name):
        avg_cost = round(self.cost / self.final_qualified_product, 2)
        gap = self.final_customer - self.final_qualified_product
        if gap > 0:
            self.cost += gap * avg_cost
    
    def print_result(self):
        print('Final qualified product:', self.final_qualified_product)
        print('Income:', self.income)
        print('Cost:', self.cost)
        print('Net Income:', self.income - self.cost)
    
    def result(self):
        return {
            'Quantity of product': self.final_qualified_product,
            'Income': self.income,
            'Cost': self.cost,
            'Net Income': self.income - self.cost,
            'Avg Cost': round(self.cost / self.final_qualified_product, 2)
        }
