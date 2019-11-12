from instruction import Instruction

class Expression(Instruction):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit_expr(self)