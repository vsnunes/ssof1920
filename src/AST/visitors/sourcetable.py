class SourceTable:
    def __init__(self):
        #this will be a list of lists
        self.branches = []
        self.variables = []
    
    def addSource(self, node):
        self.branches.append([node])

    def addSourceIfNew(self, node):
        for entry in self.branches:
            if node in entry:
                return False
        
        self.branches.append([node])
        return True

    def getSources(self, node):
        sources = []
        for entry in self.branches:
            if node in entry and entry[0] not in sources:
                sources.append(entry[0])
        return sources

    def addVarToSources(self, node, variables, sources):
        #Delete variable from all entries
        #Append variable to each source entry

        # source -> b
        # c -> a
        # d -> a

        for source in sources:
            for entry in self.branches:
                if entry[0] == source:
                    entry.append(node)

        for var in variables:
            for entry in self.branches:
                if var in entry[1:]:
                    entry.append(node)        


    def extractSources(self, sourcetables):
        for stable in sourcetables.branches:
            if len(sourcetables.variables) > 0:
                stable.append(sourcetables.variables[0])
            self.branches.append(stable)

    def delete(self, node):
        branches = []
        for entry in self.branches:
            newentry = entry[1:]
            if node in newentry:
                entry2 = [entry[0]] + list(filter((node).__ne__, newentry))
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
