class SourceTable:
    def __init__(self):
        #this will be a list of lists
        self.branches = []
        self.variables = []
    
    def addSource(self, id):
        self.branches.append([id])

    def extractSources(self, sourcetables):
        for stable in sourcetables.branches:
            if len(sourcetables.variables) > 0:
                stable.append(sourcetables.variables[0])
            self.branches.append(stable)


