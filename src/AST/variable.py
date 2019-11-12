from instruction import Instruction
from visitors.visitor import Visitor

class Variable(Instruction):
    def __init__(self, id):
        # variable identifier
        self.id = id
        self.tainted = False

    def accept(self, visitor):
        visitor.visit_variable(self)
