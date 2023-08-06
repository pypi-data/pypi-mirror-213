from abc import ABC, abstractmethod


class IJsonMathPy(ABC):
    
    @abstractmethod
    def iterpret_ast(self):
        pass

    @abstractmethod
    def parse_string(self):
        pass

    @abstractmethod
    def execute(self):
        pass