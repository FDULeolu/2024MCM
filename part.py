class Part:
    def __init__(self, name, qualified, material=None):
        self.name = name
        self.qualified = qualified
        self.material = material
    
    def is_qualified(self):
        return self.qualified

    def get_name(self):
        return self.name
    
    def get_material(self):
        return self.material
    