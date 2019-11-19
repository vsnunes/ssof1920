from instruction import Instruction

class Expression(Instruction):
    def __init__(self, child, tainted=None):
        self.child = child
        if tainted is None:
            self.tainted = self.child.tainted
        else:
            self.tainted = tainted

    def accept(self, visitor, sourcetable=None):
        visitor.visit_expr(self,sourcetable)