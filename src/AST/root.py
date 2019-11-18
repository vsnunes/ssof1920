class Root:
    def __init__(self, body):
        self.body = body

    def traverse(self, visitor):
        """
        Traverses the root instruction by instruction
        applying the visitor.

        Parameters:
        visitor (Visitor): Visitor to traverse the objects
        """
        
        self.body.accept(visitor)