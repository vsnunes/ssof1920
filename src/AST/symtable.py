class SymTable:
    def __init__(self):
        self.variables = []

    def addEntry(self, variable):
        self.variables.append(variable)
        
    def contains(self, variable_id):
        for variable in self.variables:
            if(variable.id == variable_id):
                return variable
        return None

    #something missing for checkings sinks
