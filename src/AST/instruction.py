from abc import ABCMeta, abstractmethod

class Instruction(metaclass=ABCMeta):
    def __init__(self):
        pass

    def getID(self):
        pass

    def __eq__(self, other):
        return self.__class__ == other.__class__

    @abstractmethod
    def accept(self, visitor):
        pass
