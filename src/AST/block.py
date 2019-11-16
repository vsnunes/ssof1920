from instruction import Instruction
from symtable import SymTable

class Block(Instruction):
    def __init__(self, symtable, instructions):
        self.symtable = symtable
        self.instructions = instructions

    def accept(self, visitor):
        visitor.visit_block(self)