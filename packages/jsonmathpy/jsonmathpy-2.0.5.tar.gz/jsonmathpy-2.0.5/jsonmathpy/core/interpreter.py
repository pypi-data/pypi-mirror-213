from cgitb import handler
from dataclasses import dataclass
from jsonmathpy.core.types import NodeKeys
from jsonmathpy.interfaces.interpreter import IInterpreter

@dataclass
class Node:
    node: str
    handler: str
    args: any


class Interpreter(IInterpreter):

    def __init__(self, node):
        self.node = node
    
    def interpret(self, mathjson):
        if isinstance(mathjson, dict):
            node_type = mathjson[NodeKeys.Node.value]
            handler   = mathjson[NodeKeys.Handler.value]
            arguments = mathjson[NodeKeys.Arguments.value]
            node_methods = dir(self.node)
            if (node_type in ['object', 'function']) and (handler not in node_methods) and (node_type in node_methods):
                return getattr(self.node, node_type)(Node(node_type, handler, [*[self.interpret(arg) for arg in arguments]]))
            elif handler in node_methods:
                return getattr(self.node, handler)(Node(node_type, handler, [*[self.interpret(arg) for arg in arguments]]))
            else:
                raise Exception(f"Method '{handler}' has not been inplemented by {self.node}. Please implement '{handler}' within {self.node.__class__} and declaire it in NodeConfiguration parameter.")
        else:
            return mathjson
