class SourceTable:
    """
    Class for storing context variables
    """
    def __init__(self):
        self.table = {}
        self.contextCounter = 0

    def createContext(self):
        self.table[self.contextCounter] = []
        self.contextCounter += 1

    def popContext(self):
        self.table.pop(self.contextCounter)
        self.contextCounter -= 1

    def addToContext(self, context, entry):
        self.table[context].append(entry)

    
