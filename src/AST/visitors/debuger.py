from visitor import Visitor

class Debugger(Visitor):
    """
    A Debugger Visitor just to ensure that the AST parser is done
    correctly.
    """
    
    def visit_if(self, if_inst):
        pass


    def visit_assign(self, assign_inst):
        pass


    def visit_while(self, while_inst):
        pass


    def visit_function_call(self, function_call):
        pass


    def visit_variable(self, variable):
        pass


    def visit_expr(self, expr):
        pass


    def visit_binop(self, binop):
        pass