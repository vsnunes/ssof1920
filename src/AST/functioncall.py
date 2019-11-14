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
        self.type = None
        self.tainted = False
        
        # Check if arguments are tainted
        for arg in self.args:
            self.tainted = self.tainted or arg.tainted

        # If function is a method of an object also checks if the object
        # is tainted
        if self.value is not None:
            self.tainted = self.tainted or self.value.tainted

    def setType(self, _type):
        self.type = _type


    def accept(self, visitor):
        visitor.visit_function_call(self)