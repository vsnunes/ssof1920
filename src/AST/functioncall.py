from instruction import Instruction
from attribute import Attribute

class FunctionCall(Instruction):
    def __init__(self, name, args, value=None):
        self.value = value
        self.name = name
        
        self.args = args
        self.type = ""
        self.tainted = False
        self.sources = []
        self.sanitizers = []
        
        # Check if arguments are tainted
        for arg in self.args:
            self.tainted = self.tainted or arg.tainted
            self.sources += arg.sources
            self.sanitizers += arg.sanitizers

        # If function is a method of an object also checks if the object
        # is tainted
        if self.value is not None:
            self.tainted = self.tainted or self.value.tainted
            self.sources += self.value.sources

    def getID(self):
        return self.name

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return (self.name == other.name)
        
        return False

    def __repr__(self):
        return "<FunctionCall name='{}' tainted={} type={}>".format(self.name, self.tainted, self.type)

    def __hash__(self):
        return hash("fcall" + self.name)

    def accept(self, visitor):
        visitor.visit_function_call(self)