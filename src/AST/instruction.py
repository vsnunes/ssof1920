from abc import ABCMeta, abstractmethod

class Instruction(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitor):
        pass
