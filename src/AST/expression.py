from instruction import Instruction

class Expression(Instruction):
    def __init__(self, tainted):
        self.tainted = tainted

    def accept(self, visitor):
        visitor.visit_expr(self)