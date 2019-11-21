from instruction import Instruction

class BooleanOperation(Instruction):
    def __init__(self, elements):
        self.elements = elements
        self.tainted = False
        
        # Check if elements are tainted
        for element in self.elements:
            self.tainted = self.tainted or element.tainted

    def accept(self, visitor, sourcetable=None):
        visitor.visit_boolop(self,sourcetable)