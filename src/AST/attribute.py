from instruction import Instruction
from variable import Variable

class Attribute(Instruction):
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.tainted = self.value.tainted
        self.sources = self.value.sources
        self.sanitizers = self.value.sanitizers

    def accept(self, visitor):
        visitor.visit_attribute(self)