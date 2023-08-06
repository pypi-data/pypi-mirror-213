from abc import ABC, abstractmethod



class IParserService(ABC):
    
    @abstractmethod
    def get_ast(self):
        pass