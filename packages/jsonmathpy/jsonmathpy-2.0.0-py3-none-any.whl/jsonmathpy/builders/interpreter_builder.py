from jsonmathpy.interfaces.interpreter import IInterpreter
from jsonmathpy.models.basic_nodes import NodeConfigurationModel


class InterpreterBuilder:

    def __init__(self, interpreter: IInterpreter, node_configuration: NodeConfigurationModel):
        self.node_configuration = node_configuration
        self.interpreter = interpreter
    
    def build(self) -> IInterpreter:
        return self.interpreter(self.node_configuration)
