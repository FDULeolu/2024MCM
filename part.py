import numpy as np

class Part:
    def __init__(self, id, fail_rate, check_cost, unit_price, qualified=None):
        self.id = id
        self.unit_price = unit_price
        self.check_cost = check_cost
        self.fail_rate = fail_rate
        self.qualified = qualified
    
    def get_part(self):
        if np.random.rand() > self.fail_rate:
            return Part(self.id, self.fail_rate, self.check_cost, self.unit_price, 1)
        else:
            return Part(self.id, self.fail_rate, self.check_cost, self.unit_price, 0)
    
    def get_price(self):
        return self.unit_price
    
    def get_check_cost(self):
        return self.check_cost

class SF_Product:
    def __init__(self, id, fail_rate, assemble_cost, check_cost, disassemble_cost, qualified=None, material=None) -> None:
        self.id = id
        self.fail_rate = fail_rate
        self.assemble_cost = assemble_cost
        self.check_cost = check_cost
        self.disassemble_cost = disassemble_cost
        self.qualified = qualified
        self.material = material
    
    def assemble(self, parts: list[Part]):
        for part in parts:
            if not part.qualified:
                return SF_Product(self.id, self.fail_rate, self.assemble_cost, self.check_cost, self.disassemble_cost, 0, parts)
        if np.random.rand() > self.fail_rate:
            return SF_Product(self.id, self.fail_rate, self.assemble_cost, self.check_cost, self.disassemble_cost, 1, parts)
        else:
            return SF_Product(self.id, self.fail_rate, self.assemble_cost, self.check_cost, self.disassemble_cost, 0, parts)
    
    def get_assemble_cost(self):
        return self.assemble_cost
    
    def get_check_cost(self):
        return self.check_cost
    
    def get_disassemble_cost(self):
        return self.disassemble_cost

class Product:
    def __init__(self, fail_rate, assemble_cost, check_cost, market_value, exchange_cost, disassemble_cost, qualified=None, material=None) -> None:
        self.fail_rate = fail_rate
        self.assemble_cost = assemble_cost
        self.check_cost = check_cost
        self.market_value = market_value
        self.exchange_cost = exchange_cost
        self.disassemble_cost = disassemble_cost
        self.qualified = qualified
        self.material = material
    
    def assemble(self, parts):
        for part in parts:
            if not part.qualified:
                return Product(self.fail_rate, self.assemble_cost, self.check_cost, self.market_value, self.exchange_cost, self.disassemble_cost, 0, parts)
        if np.random.rand() > self.fail_rate:
            return Product(self.fail_rate, self.assemble_cost, self.check_cost, self.market_value, self.exchange_cost, self.disassemble_cost, 1, parts)
        else:
            return Product(self.fail_rate, self.assemble_cost, self.check_cost, self.market_value, self.exchange_cost, self.disassemble_cost, 0, parts)
    
    def get_assemble_cost(self):
        return self.assemble_cost
    
    def get_check_cost(self):
        return self.check_cost
    
    def get_disassemble_cost(self):
        return self.disassemble_cost
