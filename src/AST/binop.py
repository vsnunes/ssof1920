from instruction import Instruction

class BinaryOperation(Instruction):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.tainted = self.left.tainted or self.right.tainted
        self.sources = self.left.sources + self.right.sources
        self.sanitizers = self.left.sanitizers + self.right.sanitizers

    def accept(self, visitor):
        visitor.visit_binop(self)
