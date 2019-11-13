from instruction import Instruction

class FunctionCall(Instruction):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def accept(self, visitor):
        visitor.visit_function_call(self)