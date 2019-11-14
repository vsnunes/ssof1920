from instruction import Instruction

class Attribute(Instruction):
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.tainted = self.value.tainted
        


    def accept(self, visitor):
        visitor.visit_attribute(self)