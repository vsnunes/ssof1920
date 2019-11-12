from instruction import Instruction
from visitors.visitor import Visitor

class Assign(Instruction):
    def __init__(self, leftValues, values):
        #python allows multiple assignments
        self.leftValues = leftValues
        self.values = values

    def accept(self, visitor):
        visitor.visit_assign(self)