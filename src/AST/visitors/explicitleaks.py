from visitor import Visitor

class MarkExplicitLeaks(Visitor):
    """
    Marks explicit leaks in slices for a given vulnerability.
    """
    def __init__(self):
        self.sourcetable = SourceTable()
    
    def visit_if(self, if_inst):
        pass
    
    def visit_assign(self, assign_inst):
        assign_inst.values.accept(self)
        assign_inst.leftValues.accept(self)

        assign_inst.leftValues.sources = assign_inst.values.sources


    def visit_while(self, while_inst):
        pass
    
    def visit_function_call(self, function_call):
        
        #print("************************\n"+"Vulnerability: {}\nSink: {}\nSources: {}".format(self.vulnerability.name, function_call.name, list(set(sourcesToReturn_ids)))+'\n'+"************************")
        #container = {'vulnerability': self.vulnerability.name, 'sink': function_call.name, 'source': list(set(sourcesToReturn_ids)), 'sanitizer': list()}
        pass   
            

        #with open(self.vulnerability.output, "r") as jsonFile:
        #    data = json.load(jsonFile)
        #tmp = data
        #data.append(container)
        #with open(self.vulnerability.output, 'w') as outfile:
        #    json.dump(data, outfile, ensure_ascii=False, indent=4)
    
    def visit_variable(self, variable):
        pass
    
    def visit_expr(self, expr):
        pass
    
    def visit_binop(self, binop):
        pass
    
    def visit_attribute(self, attribute):
        pass
    
    def visit_block(self, block):
        self.sourcetable.createContext()
        for instruction in block.instructions:
            instruction.accept(self)
        self.sourcetable.popContext()
    
    def visit_tuple(self, tuple):
        pass
    
    def visit_list(self, list):
        pass
    
    def visit_boolop(self, boolop):
        pass