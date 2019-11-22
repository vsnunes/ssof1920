class SourceTable:
    """
    Class for storing context variables
    """
    def __init__(self):
        self.table = {}
        self.currentContext = -1

    def createContext(self):
        self.currentContext += 1
        self.table[self.currentContext] = []

    def popContext(self):
        self.table.pop(self.currentContext)
        self.currentContext -= 1

    def add(self, entry):
        self.table[self.currentContext].append(entry)

    def addIfNotExists(self, entry):
        if entry not in self.table[self.currentContext]:
            self.table[self.currentContext].append(entry)

    def removeFromContext(self, entry):
        if entry in self.table[self.currentContext]:
            self.table[self.currentContext].remove(entry)

    
