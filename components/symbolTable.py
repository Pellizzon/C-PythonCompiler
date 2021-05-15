class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def set(self, key, val):
        self.symbols[key] = val

    def get(self, key):
        if key in self.symbols:
            return self.symbols[key]
        else:
            raise ValueError(f"Tried to access inexistent variable '{key}'")

    def declare(self, key, val):
        if key not in self.symbols:
            self.symbols[key] = val
        else:
            raise ValueError(f"Redeclaration of variable '{key}'")

    def contains(self, key):
        if key in self.symbols:
            return True
        else:
            return False

    def getType(self, key):
        if key in self.symbols:
            return self.symbols[key][1]
        else:
            raise ValueError(f"Tried to access inexistent variable '{key}'")
