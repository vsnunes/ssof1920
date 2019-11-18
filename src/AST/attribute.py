from instruction import Instruction
from variable import Variable

class Attribute(Instruction):
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.tainted = self.value.tainted

        self.tothetop = None
        

        if type(self.value) == Attribute:
            self.tothetop = self.value.tothetop
        else:
            self.tothetop = self.value

    def accept(self, visitor, sourcetable=None):
        visitor.visit_attribute(self,sourcetable)