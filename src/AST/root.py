class Root:
    def __init__(self, instructions):
        self.instructions = instructions

    def traverse(self, visitor):
        """
        Traverses the root instruction by instruction
        applying the visitor.

        Parameters:
        visitor (Visitor): Visitor to traverse the objects
        """
        for instruction in self.instructions:
            instruction.accept(visitor)