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
        self.display("Condition")
        self.innerScope()
        if_inst.condition.accept(self)
        self.outerScope()
        self.display("Body")
        if_inst.body.accept(self)
        if len(if_inst.orelse.instructions) > 0:
            self.display("Else")
            if_inst.orelse.accept(self)
        self.outerScope()

    def visit_assign(self, assign_inst):
        self.display("*Assign")
        self.innerScope()
        self.display("LeftValues")
        self.innerScope()
        for leftValue in assign_inst.leftValues:
            leftValue.accept(self)
        self.outerScope()
        self.display("RightValue")
        self.innerScope()
        assign_inst.values.accept(self)
        self.outerScope()
        self.outerScope()


    def visit_while(self, while_inst):
        self.display("*While")
        self.innerScope()
        self.display("Condition")
        self.innerScope()
        while_inst.condition.accept(self)
        self.outerScope()
        self.display("Body")
        self.innerScope()
        while_inst.body.accept(self)
        self.outerScope()
        if len(while_inst.orelse.instructions) > 0:
            self.display("Else")
            while_inst.orelse.accept(self)
            self.outerScope()
        self.outerScope()



    def visit_function_call(self, function_call):
        self.display("*FunctionCall name = " + function_call.name + " Type = " + function_call.type + " Tainted? = " + str(function_call.tainted))
        self.innerScope()
        if len(function_call.args) > 0:
            self.display("Args")
            self.innerScope()
            for arg in function_call.args:
                arg.accept(self)
            self.outerScope()
        if function_call.value is not None: 
            self.display("Value")
            self.innerScope()
            function_call.value.accept(self)
            self.outerScope()
        self.outerScope()
        
    def visit_variable(self, variable):
        self.display("*Variable Id = " + variable.id + " Type = " + variable.type + " Tainted? = " + str(variable.tainted) + " Sources = " + str(variable.sources))


    def visit_expr(self, expr):
        self.display("*Expr Tainted? = " + str(expr.tainted))
        if expr.child is not None:
            self.innerScope()
            self.display("Child")
            self.innerScope()
            expr.child.accept(self)
            self.outerScope()
            self.outerScope()

    def visit_binop(self, binop):
        self.display("*BinOp Tainted? = " + str(binop.tainted))
        self.innerScope()
        binop.left.accept(self)
        binop.right.accept(self)
        self.outerScope()

    def visit_attribute(self, attribute):
        self.display("*Attribute Tainted? = " + str(attribute.tainted) + " Id = " + str(attribute.attr))
        self.innerScope()
        attribute.value.accept(self)
        self.outerScope()

    def visit_block(self, block):
        self.display("*Block")
        self.innerScope()
        for instruction in block.instructions:
            instruction.accept(self)
        self.outerScope()

    def visit_tuple(self, tuple):
        self.display("*Tuple")
        self.innerScope()
        self.display("Elements")
        self.innerScope()
        for element in tuple.elements:
            element.accept(self)
        self.outerScope()
        self.outerScope()

    def visit_list(self, list):
        self.display("*List")
        self.innerScope()
        self.display("Elements")
        self.innerScope()
        for element in list.elements:
            element.accept(self)
        self.outerScope()
        self.outerScope()

    def visit_boolop(self, boolop):
        self.display("*BooleanOperation")
        self.innerScope()
        self.display("Elements")
        self.innerScope()
        for element in boolop.elements:
            element.accept(self)
        self.outerScope()
        self.outerScope()

    def visit_compare(self, compare):
        self.display("*Compare")
        self.innerScope()
        self.display("Left")
        self.innerScope()
        compare.left.accept(self)
        self.outerScope()
        self.display("Comparators")
        self.innerScope()
        for comparator in compare.comparators:
            comparator.accept(self)
        self.outerScope()