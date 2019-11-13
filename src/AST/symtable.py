class SymTable:
    def __init__(self):
        self.variables = []

    def addEntry(self, variable):
        self.variables.append(variable)
        
    def contains(self, variable_id):
        variable = self.variables[0]
        self.variables = self.variables[1:]
        return variable

    def giveMeLast(self,variable_id):
        for i in range(len(self.variables)-1, -1, -1):
            if self.variables[i].id == variable_id:
                return self.variables[i].tainted
        return None

    def reWrite(self, variable_id, tainted):
        for i in range(len(self.variables)-1, -1, -1):
            if self.variables[i].id == variable_id:
                self.variables[i].tainted = tainted
                break


    #something missing for checkings sinks