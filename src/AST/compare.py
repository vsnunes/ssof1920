from instruction import Instruction

class Compare(Instruction):
    def __init__(self, left, comparators):
        self.left = left
        self.comparators = comparators
        self.tainted = False
        self.sources = self.left.sources
        self.sanitizers = self.left.sanitizers

        for comparator in self.comparators:
            self.tainted = self.tainted or self.left.tainted or comparator.tainted
            self.sources += comparator.sources
            self.sanitizers + comparator.sanitizers

    def accept(self, visitor):
        visitor.visit_compare(self)