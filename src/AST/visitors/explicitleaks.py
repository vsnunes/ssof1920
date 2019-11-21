import json
from visitor import Visitor
from sourcetable import SourceTable
from copy import deepcopy

class DetectExplicitLeaks(Visitor):
    """
    Detects explicit leaks in slices for a given vulnerability.
    """

    def __init__(self, vulnerability):
        self.vulnerability = vulnerability
        self.assignTable = None
        self.assignID = None
        self.toDelete = True

    
    def visit_if(self, if_inst, sourcetable=None):
        sourcetableCondition = SourceTable()
        sourcetableCondition.branches = deepcopy(sourcetable.branches)
        sourcetableCondition.variables = deepcopy(sourcetable.variables)

        if_inst.condition.accept(self,sourcetableCondition)

        sourcetableBody = SourceTable()
        sourcetableBody.branches = deepcopy(sourcetable.branches)
        sourcetableBody.variables = deepcopy(sourcetable.variables)
        if_inst.body.accept(self,sourcetableBody)

        if len(if_inst.orelse.instructions) > 0:
            sourcetableElse = SourceTable()
            sourcetableElse.branches = deepcopy(sourcetable.branches)
            sourcetableElse.variables = deepcopy(sourcetable.variables)
            if_inst.orelse.accept(self,sourcetableElse)

            sourcetable.branches = sourcetableBody.branches + sourcetableElse.branches
            sourcetable.variables = sourcetableBody.variables + sourcetableElse.variables

        else:
            
            sourcetable.branches += sourcetableBody.branches
            sourcetable.variables += sourcetableBody.variables

        
        #

    
    def visit_assign(self, assign_inst, sourcetable=None):
        self.assignTable = sourcetable
        self.assignID = assign_inst.leftValues.id

        #this symtable have the purpose of tracking it values are sources
        dummyStable = SourceTable()
        assign_inst.leftValues.accept(self,dummyStable)


        #pass dummyStable to right side
        dummyStable = SourceTable()
        #dummyStable.branches = deepcopy(sourcetable.branches)
        assign_inst.values.accept(self,dummyStable)
        sources_id = []
        for sources in dummyStable.branches:
                #no key chain, just the head (source)
                source = sources[0]
                if sourcetable.addSourceIfNew(source):
                    sources_id.append(source)
                
        if self.toDelete:
            sourcetable.delete(assign_inst.leftValues.id)
            self.toDelete = True

        listOfSources = sourcetable.addVarToSources(assign_inst.leftValues.id, dummyStable.variables, sources_id)

        self.assignTable = None
        self.assignID = None


    
    def visit_while(self, while_inst, sourcetable=None):
        sourcetableCondition = SourceTable()
        sourcetableCondition.branches = deepcopy(sourcetable.branches)
        sourcetableCondition.variables = deepcopy(sourcetable.variables)

        while_inst.condition.accept(self,sourcetableCondition)

        sourcetableBody = SourceTable()
        sourcetableBody.branches = deepcopy(sourcetable.branches)
        sourcetableBody.variables = deepcopy(sourcetable.variables)
        while_inst.body.accept(self,sourcetableBody)

        if len(while_inst.orelse.instructions) > 0:
            sourcetableElse = SourceTable()
            sourcetableElse.branches = deepcopy(sourcetable.branches)
            sourcetableElse.variables = deepcopy(sourcetable.variables)
            while_inst.orelse.accept(self,sourcetableElse)

            sourcetable.branches = sourcetableBody.branches + sourcetableElse.branches
            sourcetable.variables = sourcetableBody.variables + sourcetableElse.variables

        else:
            
            sourcetable.branches += sourcetableBody.branches
            sourcetable.variables += sourcetableBody.variables

    
    def visit_function_call(self, function_call, sourcetable=None):
        if function_call.type == "source":
            sourcetable.addSource(function_call.name)
        
        if function_call.type == "sink" and function_call.tainted == True:

            if self.assignTable == None:
                tmpSource = sourcetable
            else:
                tmpSource = self.assignTable
                self.toDelete = False

            sourcesToReturn = []
            dummyStable = SourceTable()
            for arg in function_call.args:
                arg.accept(self,dummyStable)

            
            #print(" before tmpSource", tmpSource)
            #iterate over sources
            for sources in dummyStable.branches:
                #no key chain, just the head (source)
                source = sources[0]
                if tmpSource.addSourceIfNew(source):
                    sourcesToReturn.append(source)
                
            #print(" after tmpSource", tmpSource)
            #in case of right value is function in an assigment
            if self.assignTable != None:
                listOfSources = tmpSource.addVarToSources(self.assignID, dummyStable.variables, sourcesToReturn)
                
            

            #iterate over not source tainted variables
            #print(dummyStable.variables)
            for taintedVar in dummyStable.variables:
                listOfSources = tmpSource.getSources(taintedVar)
                sourcesToReturn += listOfSources

            
            #now all variables in arguments are represented as sources in dummyStable
            
            
            print("************************\n"+"Vulnerability: {}\nSink: {}\nSources: {}".format(self.vulnerability.name, function_call.name, list(set(sourcesToReturn)))+'\n'+"************************")
            container = {'vulnerability': self.vulnerability.name, 'sink': function_call.name, 'source': list(set(sourcesToReturn)), 'sanitizer': list()}

            with open(self.vulnerability.output, "r") as jsonFile:
                data = json.load(jsonFile)
            tmp = data
            data.append(container)
            with open(self.vulnerability.output, 'w') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4)
            
        
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
        if sourcetable is None:
            sourcetable = SourceTable()
        for instruction in block.instructions:
            instruction.accept(self,sourcetable)