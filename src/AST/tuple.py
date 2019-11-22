from instruction import Instruction

class Tuple(Instruction):
    def __init__(self, elements):
        self.elements = elements
        self.tainted = False

        for element in self.elements:
            self.tainted = self.tainted or element.tainted

    def accept(self, visitor):
        visitor.visit_tuple(self)