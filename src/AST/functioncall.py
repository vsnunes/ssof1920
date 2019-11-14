from instruction import Instruction

class FunctionCall(Instruction):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.type = None
        self.tainted = False
        for arg in self.args:
            self.tainted = self.tainted or arg.tainted

    def setType(self, _type):
        self.type = _type

    def accept(self, visitor):
        visitor.visit_function_call(self)