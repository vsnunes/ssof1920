from instruction import Instruction

class List(Instruction):
    def __init__(self, elements):
        self.elements = elements
        self.tainted = False
        self.sources = []
        self.sanitizers = []

        for element in self.elements:
            self.tainted = self.tainted or element.tainted
            self.sources += element.sources
            self.sanitizers += element.sanitizers

    def accept(self, visitor):
        visitor.visit_list(self)