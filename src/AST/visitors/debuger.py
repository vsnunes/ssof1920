from visitor import Visitor

class Debugger(Visitor):
    """
    A Debugger Visitor just to ensure that the AST parser is done
    correctly.
    """

    def __init__(self):
        self.identation = ""

    def display(self, msg):
        print(self.identation + msg)
        self.identation += "    "

    def visit_if(self, if_inst):
        self.display("If")
        if_inst.condition.accept(self)
        if if_inst.body is not None:
            if_inst.body.accept(self)
        if if_inst.orelse is not None:
            if_inst.orelse.accept(self)

    def visit_assign(self, assign_inst):
        self.display("Assign")
        assign_inst.leftValues.accept(self)
        assign_inst.values.accept(self)


    def visit_while(self, while_inst):
        pass


    def visit_function_call(self, function_call):
        pass


    def visit_variable(self, variable):
        self.display("Variable Id = " + variable.id)


    def visit_expr(self, expr):
        self.display("Expr Val = " + str(expr.value))


    def visit_binop(self, binop):
        self.display("BinOp")
        binop.left.accept(self)
        binop.right.accept(self)