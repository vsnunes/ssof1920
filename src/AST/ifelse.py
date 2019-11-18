from instruction import Instruction
from visitors.visitor import Visitor

class If (Instruction):
    def __init__(self, condition, body, orelse):
        self.condition = condition
        self.body = body
        self.orelse = orelse

    def accept(self, visitor, sourcetable=None):
        visitor.visit_if(self,sourcetable)