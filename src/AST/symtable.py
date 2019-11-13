class SymTable:
    def __init__(self):
        self.variables = []
        self.pointer = 0

    def addEntry(self, variable):
        self.variables.append(variable)
        
    def contains(self, variable_id):
        variable = self.variables[0]
        self.variables = self.variables[1:]
        return variable

        #for i in range(self.pointer, -1, -1):
        #    if variable.id == variable_id:
        #        return variable.tainted

    #something missing for checkings sinks