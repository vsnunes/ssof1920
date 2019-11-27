from AST.variable import Variable
from AST.functioncall import FunctionCall
from AST.attribute import Attribute

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
            for source in obj.sources:
                if source not in sources:
                    sources.append(source)
        return sources

    def getSanitizers(self):
        sanitizers = []
        for obj in self.stack:
            for sanitizer in obj.sanitizers:
                if sanitizer not in sanitizers:
                    sanitizers.append(sanitizer)
        return sanitizers

    def copyObject(self, obj):
        if obj.__class__.__name__ == "Variable":
            newobj = Variable(obj.getID())
        elif obj.__class__.__name__ == "FunctionCall":
            newargs = []
            for arg in obj.args:
                # to prevent infinite recursion
                if arg.getID() != obj.getID():
                    newargs.append(self.copyObject(arg))

            newobj = FunctionCall(obj.getID(), newargs, self.copyObject(obj.value))

        elif obj.__class__.__name__ == "Attribute":
            newobj = Attribute(self.copyObject(obj.attr), self.copyObject(obj.value))

        for source in obj.sources:
            #to prevent infinite recursion
            if source.getID() != obj.getID():
                newobj.sources.append(self.copyObject(source))
        for sanitizer in obj.sanitizers:
            #to prevent infinite recursion
            if sanitizer.getID() != obj.getID():
                newobj.sanitizers.append(self.copyObject(sanitizer))