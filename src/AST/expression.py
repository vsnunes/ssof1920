from instruction import Instruction

class Expression(Instruction):
    def __init__(self, child, tainted=None):
        self.child = child
        if tainted is None:
            self.tainted = self.child.tainted
        else:
            self.tainted = tainted

        if self.child is None:
            self.sources = []
            self.sanitizers = []
        else:
            self.sources = self.child.sources
            self.sanitizers = self.child.sanitizers

    def accept(self, visitor):
        visitor.visit_expr(self)