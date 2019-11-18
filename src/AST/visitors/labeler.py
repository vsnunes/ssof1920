from visitor import Visitor

class Labeler(Visitor):
    """
    A Labeler Visitor to atribute labels {sink,source,sanitizer} to function nodes
    """

    def __init__(self, vulnerability):
        self.vulnerability = vulnerability

    def visit_if(self, if_inst,sourcetable=None):
        if_inst.condition.accept(self)
        if_inst.body.accept(self)
        if len(if_inst.orelse.instructions) > 0:
            if_inst.orelse.accept(self)

    def visit_assign(self, assign_inst,sourcetable=None):
        assign_inst.leftValues.accept(self)
        assign_inst.values.accept(self)

    def visit_while(self, while_inst,sourcetable=None):
        while_inst.condition.accept(self)
        while_inst.body.accept(self)
        if len(while_inst.orelse.instructions) > 0:
            while_inst.orelse.accept(self)

    def visit_function_call(self, function_call,sourcetable=None):
        function_call.type = self.vulnerability.getType(function_call.name)

        #source functions are always tainted
        if function_call.type == "source":
            function_call.tainted = True

        for arg in function_call.args:
            arg.accept(self)
        if function_call.value is not None:
            function_call.value.accept(self) 
            
    def visit_variable(self, variable,sourcetable=None):
        pass

    def visit_expr(self, expr,sourcetable=None):
        if expr.child is not None:
            expr.child.accept(self)

    def visit_binop(self, binop,sourcetable=None):
        binop.left.accept(self)
        binop.right.accept(self)

    
    def visit_attribute(self, attribute,sourcetable=None):
        attribute.value.accept(self)


    def visit_block(self, block,sourcetable=None):
        for instruction in block.instructions:
            instruction.accept(self)