from abc import abstractmethod
# Generic Visitor for Instructions
class Visitor(metaclass=abc.ABCMeta):
    
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
