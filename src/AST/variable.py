from instruction import Instruction
from visitors.visitor import Visitor

class Variable(Instruction):
    def __init__(self, id):
        # variable identifier
        self.id = id
        self.tainted = True
        self.type = ""

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return (self.id == other.id)
        
        return False

    def __hash__(self):
        return hash("var" + self.id)

    def __repr__(self):
        return "<Variable id='{}' tainted={} type={}>".format(self.id, self.tainted, self.type)

    def getID(self):
        return self.id

    def accept(self, visitor, sourcetable=None):
        visitor.visit_variable(self, sourcetable)
