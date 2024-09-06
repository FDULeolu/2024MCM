class Strategy:
    def __init__(self, strategy) -> None:
        self.check_parts = strategy['check_parts']
        self.check_products = strategy['check_products']
        self.disassemble = strategy['disassemble']
    
