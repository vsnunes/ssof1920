from instruction import Instruction

class List(Instruction):
    def __init__(self, elements):
        self.elements = elements
        self.tainted = False

        for element in self.elements:
            self.tainted = self.tainted or element.tainted

    def accept(self, visitor, sourcetable=None):
        visitor.visit_list(self,sourcetable)