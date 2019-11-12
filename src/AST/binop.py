from instruction import Instruction

class BinaryOperation(Instruction):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        visitor.visit_binop(self)
