class Node:
    def __init__(self, initValue, initChildren=[]):
        self.value = initValue
        self.children = initChildren

    def Evaluate(self):
        return


class BinOp(Node):
    def Evaluate(self):
        firstChildEval = self.children[0].Evaluate()
        secondChildEval = self.children[1].Evaluate()

        if self.value == "PLUS":
            evaluate = firstChildEval + secondChildEval
        elif self.value == "MINUS":
            evaluate = firstChildEval - secondChildEval
        elif self.value == "DIV":
            evaluate = firstChildEval / secondChildEval
        elif self.value == "MULT":
            evaluate = firstChildEval * secondChildEval
        else:
            raise ValueError("Could not evaluate BinOp")

        return int(evaluate)


class UnOp(Node):
    def Evaluate(self):
        childEval = self.children[0].Evaluate()

        if self.value == "PLUS":
            evaluate = +childEval
        elif self.value == "MINUS":
            evaluate = -childEval
        else:
            raise ValueError("Could not evaluate UnOp")

        return int(evaluate)


class IntVal(Node):
    def Evaluate(self):
        return int(self.value)


class NoOp(Node):
    def Evaluate(self):
        return super().Evaluate()