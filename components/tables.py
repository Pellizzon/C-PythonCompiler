class FunctionTable:
    def __init__(self):
        self.functions = {}

    def newFunc(self, funcName, block, funcType, args):
        if funcName not in self.functions:
            self.functions[funcName] = {
                "block": block,
                "type": funcType,
                "args": args,
            }
        else:
            raise ValueError(f"Redeclaration of function '{funcName}'")

    def getFuncArgs(self, key):
        if self.contains(key):
            return self.functions[key]["args"]
        else:
            raise ValueError(f"Function {key} not found")

    def getFuncBlock(self, key):
        if self.contains(key):
            return self.functions[key]["block"]
        else:
            raise ValueError(f"Function {key} not found")

    def getFuncType(self, key):
        if self.contains(key):
            return self.functions[key]["type"]
        else:
            raise ValueError(f"Function {key} not found")

    def contains(self, key):
        if key in self.functions:
            return True
        else:
            return False


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def set_(self, key, val):
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
