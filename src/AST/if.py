from instruction import Instruction

class If (Instruction):
    def __init__(self):
        self.condition = None
        self.body = None
        self.orelse = None
