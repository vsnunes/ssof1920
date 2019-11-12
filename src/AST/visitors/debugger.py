from visitor import Visitor

class Debugger(Visitor):
    """
    A Debugger Visitor just to ensure that the AST parser is done
    correctly.
    """

    def __init__(self):
        self.identation = 0

    def display(self, msg):
        print(self.identation*' ' + msg)

    def innerScope(self):
        self.identation += 4

    def outerScope(self):
        self.identation -= 4

    def visit_if(self, if_inst):
        self.display("*If")
        self.innerScope()
        if_inst.condition.accept(self)
        if if_inst.body is not None:
            for instruction in if_inst.body:
                instruction.accept(self)
        if if_inst.orelse is not None:
            self.display("Else")
            for instruction in if_inst.orelse:
                instruction.accept(self)
        self.outerScope()

    def visit_assign(self, assign_inst):
        self.display("*Assign")
        self.innerScope()
        assign_inst.leftValues.accept(self)
        assign_inst.values.accept(self)
        self.outerScope()


    def visit_while(self, while_inst):
        pass


    def visit_function_call(self, function_call):
        pass


    def visit_variable(self, variable):
        self.display("*Variable Id = " + variable.id + " Tainted? = " + str(variable.tainted))


    def visit_expr(self, expr):
        self.display("*Expr Tainted? = " + str(expr.tainted))


    def visit_binop(self, binop):
        self.display("*BinOp Tainted? = " + str(binop.tainted))
        self.innerScope()
        binop.left.accept(self)
        binop.right.accept(self)
        self.outerScope()