from abc import ABC, abstractmethod


class IInterpreterService(ABC):
    
    @abstractmethod
    def interpret_ast_based_on_user_defined_config(self):
        pass