from instruction import Instruction
from variable import Variable

class Attribute(Instruction):
    def __init__(self, attr, value):
        self.attr = attr
        self.value = value
        self.tainted = self.value.tainted or self.attr.tainted
        self.sanitizers = self.value.sanitizers

        #self.value.sources += self.attr.sources
        #self.value.tainted = self.attr.tainted
        #self.sources = self.value.sources
        self.sources = self.value.sources + self.attr.sources

    def accept(self, visitor):
        visitor.visit_attribute(self)