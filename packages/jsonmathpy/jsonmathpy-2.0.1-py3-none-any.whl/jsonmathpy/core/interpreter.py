from jsonmathpy.interfaces.interpreter import IInterpreter
from jsonmathpy.models.node_keys import ConfigurationModels

class Interpreter(IInterpreter):

    def __init__(self, node):
        self.node = node
    
    def interpret(self, mathjson):
        if isinstance(mathjson, dict):
            operation = mathjson["node"]
            arguments = mathjson["args"]
            node_methods = dir(self.node)
            if operation in node_methods:
                return getattr(self.node, operation)(*[self.interpret(arg) for arg in arguments])
            else:
                raise Exception(f"Method '{operation}' has not been inplemented by {self.node}. Please implement '{operation}' within {self.node.__class__} and declaire it in NodeConfiguration parameter.")
        else:
            return mathjson
