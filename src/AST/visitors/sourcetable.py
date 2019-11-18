class SourceTable:
    def __init__(self):
        #this will be a list of lists
        self.branches = []
        self.variables = []
    
    def addSource(self, id):
        self.branches.append([id])

    def addSourceIfNew(self, id):
        for entry in self.branches:
            if entry[0] == id:
                return False
        
        self.branches.append([id])
        return True

    def getSources(self, id):
        sources = []
        for entry in self.branches:
            #print("ENTRY: " + str(entry))
            if id in entry and entry[0] not in sources:
                sources.append(entry[0])
        return sources

    def addVarToSources(self, variable_id, variables, sources):
        #Delete variable from all entries
        #Append variable to each source entry

        # source -> b
        # c -> a
        # d -> a

        for source in sources:
            for entry in self.branches:
                if entry[0] == source:
                    entry.append(variable_id)

        for var in variables:
            for entry in self.branches:
                if var in entry[1:]:
                    entry.append(variable_id)        


    def extractSources(self, sourcetables):
        for stable in sourcetables.branches:
            if len(sourcetables.variables) > 0:
                stable.append(sourcetables.variables[0])
            self.branches.append(stable)

    def delete(self, id):
        branches = []
        for entry in self.branches:
            newentry = entry[1:]
            if id in newentry:
                entry2 = [entry[0]] + list(filter((id).__ne__, newentry))
            else:
                entry2 = entry

            branches.append(entry2)
        self.branches = branches
            
            

    def __str__(self):
        toPrint = "branches-> "
        for branch in self.branches:
            toPrint += str(branch) + ' '
        toPrint += "variables-> " + str(self.variables)

        return toPrint
