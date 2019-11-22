from instruction import Instruction
from attribute import Attribute

class FunctionCall(Instruction):
    def __init__(self, name, args, value=None):
        self.value = value
        if value is not None:
            self.name = self.value.id
        else:
            self.name = name
        
        self.args = args
        self.type = ""
        self.tainted = False
        
        # Check if arguments are tainted
        for arg in self.args:
            self.tainted = self.tainted or arg.tainted

        # If function is a method of an object also checks if the object
        # is tainted
        if self.value is not None:
            self.tainted = self.tainted or self.value.tainted

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

    def accept(self, visitor, sourcetable=None):
        visitor.visit_function_call(self,sourcetable)