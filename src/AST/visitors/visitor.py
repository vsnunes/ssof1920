from abc import ABCMeta, abstractmethod
# Generic Visitor for Instructions
class Visitor(metaclass=ABCMeta):
    
    @abstractmethod
    def visit_if(self, if_inst):
        pass

    @abstractmethod
    def visit_assign(self, assign_inst):
        pass

    @abstractmethod
    def visit_while(self, while_inst):
        pass

    @abstractmethod
    def visit_function_call(self, function_call):
        pass

    @abstractmethod
    def visit_variable(self, variable):
        pass

    @abstractmethod
    def visit_expr(self, expr):
        pass

    @abstractmethod
    def visit_binop(self, binop):
        pass

    @abstractmethod
    def visit_attribute(self, attribute):
        pass

    @abstractmethod
    def visit_block(self, block):
        pass

    @abstractmethod
    def visit_tuple(self, tuple):
        pass

    @abstractmethod
    def visit_list(self, list):
        pass

    @abstractmethod
    def visit_boolop(self, boolop):
        pass