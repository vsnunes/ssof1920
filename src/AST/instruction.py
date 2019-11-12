from abc import abstractmethod

class Instruction(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitor):
        pass
