from instruction import Instruction
from visitors.visitor import Visitor

class While(Instruction):
    def __init__(self):
        self.condition = None
        self.body = None
        self.orelse = None

    def accept(self, visitor):
        visitor.visit_while(self)