from visitor import Visitor
from sourcetable import SourceTable

class DetectExplicitLeaks(Visitor):
    """
    Detects explicit leaks in slices for a given vulnerability.
    """

    def __init__(self, vulnerability):
        self.vulnerability = vulnerability
        #######

    
    def visit_if(self, if_inst, sourcetable=None):
        if_inst.condition.accept(self,sourcetable)
        if_inst.body.accept(self,sourcetable)
        if len(if_inst.orelse.instructions) > 0:
            if_inst.orelse.accept(self,sourcetable)

    
    def visit_assign(self, assign_inst, sourcetable=None):
        #this symtable have the purpose of tracking it values are sources
        dummyStable = SourceTable()
        assign_inst.leftValues.accept(self,dummyStable)
        
        #pass dummyStable to right side
        dummyStable = SourceTable()
        assign_inst.values.accept(self,dummyStable)
        sources_id = []
        for sources in dummyStable.branches:
                #no key chain, just the head (source)
                source = sources[0]
                sources_id.append(source)
                sourcetable.addSourceIfNew(source)

        #iterate over not source tainted variables
        #variable (left value) = [a]
        #sources = [b,c,d]

        # (a, [b], [c, d])
        #source -> b
        # c -> a
        # d -> a
        listOfSources = sourcetable.addVarToSources(assign_inst.leftValues.id, dummyStable.variables, sources_id)

    
    def visit_while(self, while_inst, sourcetable=None):
        while_inst.condition.accept(self,sourcetable)
        while_inst.body.accept(self,sourcetable)
        if len(while_inst.orelse.instructions) > 0:
            while_inst.orelse.accept(self,sourcetable)

    
    def visit_function_call(self, function_call, sourcetable=None):
        if function_call.type == "source":
            sourcetable.addSource(function_call.name)


        if function_call.type == "sink" and function_call.tainted == True:
            sourcesToReturn = []
            dummyStable = SourceTable()
            for arg in function_call.args:
                arg.accept(self,dummyStable)

            #iterate over sources
            for sources in dummyStable.branches:
                #no key chain, just the head (source)
                source = sources[0]
                sourcesToReturn.append(source)
                sourcetable.addSourceIfNew(source)

            #iterate over not source tainted variables
            #print(dummyStable.variables)
            for taintedVar in dummyStable.variables:
                listOfSources = sourcetable.getSources(taintedVar)
                sourcesToReturn += listOfSources
        
            #now all variables in arguments are represented as sources in dummyStable
            
            
            print("************************\n"+"Vulnerability: {}\nSink: {}\nSources: {}".format(self.vulnerability.name, function_call.name, list(set(sourcesToReturn)))+'\n'+"************************")
            #print(sourcetable)
        else:
            for arg in function_call.args:
                arg.accept(self,sourcetable)
        if function_call.value is not None:
            function_call.value.accept(self,sourcetable) 
    
    def visit_variable(self, variable, sourcetable=None):
        if variable.type == "source":
            sourcetable.addSource(variable.id)
            sourcetable.variables.append(variable.id)
        elif variable.tainted:
            sourcetable.variables.append(variable.id)

    
    def visit_expr(self, expr, sourcetable=None): 
        if expr.child is not None:
            expr.child.accept(self,sourcetable)

    
    def visit_binop(self, binop, sourcetable=None):
        binop.left.accept(self,sourcetable)
        binop.right.accept(self,sourcetable)

    
    def visit_attribute(self, attribute, sourcetable=None):
        attribute.value.accept(self,sourcetable)

    
    def visit_block(self, block, sourcetable=None):
        sourcetable = SourceTable()
        for instruction in block.instructions:
            instruction.accept(self,sourcetable)