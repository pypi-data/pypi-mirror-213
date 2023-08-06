from jsonmathpy.interfaces.interpreter import IInterpreter
from jsonmathpy.models.node_keys import ConfigurationModels

class Interpreter(IInterpreter):

    def __init__(self, operations: ConfigurationModels):
        self.operations = operations.get_node_handlers()
    
    def interpret(self, mathjson):
        if isinstance(mathjson, dict):
            operation = mathjson["node"]
            arguments = mathjson["args"]
            if operation in self.operations:
                if operation in self.operations.keys():
                    return self.operations[operation](*[self.interpret(arg) for arg in arguments]).execute()
                else:
                    raise TypeError(f'You have not defined the operation {operation}. Please write a class which handles this node operation and pass into args.')
        else:
            return mathjson
