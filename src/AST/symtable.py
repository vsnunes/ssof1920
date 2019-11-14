class SymTable:
    def __init__(self):
        self.variables = []
        self.pointer = 0

    def addEntry(self, variable):
        self.variables.append(variable)
        
    def contains(self, variable_id):
        variable = self.variables[self.pointer]
        self.pointer += 1
        return variable

    def giveMeLast(self,variable_id):
        for i in range(len(self.variables)-1, self.pointer -1, -1):
            if self.variables[i].id == variable_id:
                return self.variables[i].tainted
        return None

    def reWrite(self, variable_id, tainted):
        for i in range(len(self.variables)-1, self.pointer -1, -1):
            if self.variables[i].id == variable_id:
                self.variables[i].tainted = tainted
                break

    def resetPointer(self):
        self.pointer = 0

    #something missing for checkings sinks