from abc import ABCMeta, abstractmethod
# Generic Visitor for Instructions
class Visitor(metaclass=ABCMeta):
    
    @abstractmethod
    def visit_if(self, if_inst,sourcetable=None):
        pass

    @abstractmethod
    def visit_assign(self, assign_inst,sourcetable=None):
        pass

    @abstractmethod
    def visit_while(self, while_inst,sourcetable=None):
        pass

    @abstractmethod
    def visit_function_call(self, function_call,sourcetable=None):
        pass

    @abstractmethod
    def visit_variable(self, variable,sourcetable=None):
        pass

    @abstractmethod
    def visit_expr(self, expr,sourcetable=None):
        pass

    @abstractmethod
    def visit_binop(self, binop,sourcetable=None):
        pass

    @abstractmethod
    def visit_attribute(self, attribute,sourcetable=None):
        pass

    @abstractmethod
    def visit_block(self, block,sourcetable=None):
        pass

    @abstractmethod
    def visit_tuple(self, tuple,sourcetable=None):
        pass

    @abstractmethod
    def visit_list(self, list,sourcetable=None):
        pass