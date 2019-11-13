from instruction import Instruction
from visitors.visitor import Visitor

class Variable(Instruction):
    def __init__(self, id):
        # variable identifier
        self.id = id
        self.tainted = True

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.id == other.id
        
        return False

    def accept(self, visitor):
        visitor.visit_variable(self)
