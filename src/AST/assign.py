from instruction import Instruction
from visitors.visitor import Visitor

class Assign(Instruction):
    def __init__(self):
        #python allows multiple assignments
        self.leftValues = []
        self.values = []

    def accept(self, visitor):
        visitor.visit_assign(self)