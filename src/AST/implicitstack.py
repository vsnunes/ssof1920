
class ImplicitStack():
    def __init__(self):
        self.stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        if len(self.stack):  
            return self.stack.pop()
        return None

    def getSources(self):
        sources = []
        for obj in self.stack:
            sources += obj.sources
        return list(set(sources))

    def getSanitizers(self):
        sanitizers = []
        for obj in self.stack:
            sanitizers += obj.sanitizers
        return list(set(sanitizers))