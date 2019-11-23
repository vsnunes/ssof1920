class SymTable:
    def __init__(self):
        self.context = 0
        self.variables = []
        self.pointer = 0

    def addEntry(self, variable):
        self.variables.append(variable)
        
    #not used
    def contains(self, variable_id):
        variable = self.variables[self.pointer]
        self.pointer += 1
        return variable

    def getVariable(self, variable_id):
        for variable in self.variables:
            if variable.id == variable_id:
                return variable
        return None

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

    def clear(self, onlyTainted=True):
        """
        Returns the symtable with only the last change of every variable
        discarding intermediate states.
        """
        #self.cleaned = []
        #self.alreadyReached = []
        #for i in range(len(self.variables) - 1, -1, -1):
            # Only merge if tainted values since we want worst case scenario
        #    if onlyTainted:
        #        if (self.variables[i].id not in self.alreadyReached) and self.variables[i].tainted:
        #            self.alreadyReached.append(self.variables[i].id)
        #            self.cleaned.append(self.variables[i])
        #    else:
        #        if (self.variables[i].id not in self.alreadyReached):
        #            self.alreadyReached.append(self.variables[i].id)
        #            self.cleaned.append(self.variables[i])

        #sym = SymTable()
        #sym.variables = self.cleaned
        #return sym

    def __add__(self, other):
        result = []
        for variable in self.variables:
            other_variable = other.getVariable(variable.id)
            if other_variable is not None:
                if variable.tainted == True:
                    if other_variable.tainted == True:
                        variable.sources = list(set(other_variable.sources + variable.sources))
                        variable.sanitizers = list(set(other_variable.sanitizers + variable.sanitizers))
                    result.append(variable)
                else:
                    result.append(other_variable)
            else:
                result.append(variable)

        for variable in other.variables:
            if variable not in result:
                result.append(variable)
        
        sym = SymTable()
        sym.variables = result
        return sym

    def concat(self, other_symtable):
        result = []
        for var in other_symtable.variables:
            if var not in self.variables:
                var.sources.append(var)
            if var.tainted:
                result.append(var)
        self.variables = result

    def resetPointer(self):
        self.pointer = 0

    def innerContext(self):
        self.context += 1
    
    def outerContext(self):
        self.context -= 1

    def __str__(self):
        s = "< "
        for var in self.variables:
            s += str(var) + " "
        return s + ">"

    #something missing for checkings sinks