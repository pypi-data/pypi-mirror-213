from dataclasses import dataclass
from jsonmathpy.builders.interpreter_builder import InterpreterBuilder
from jsonmathpy.core.interpreter import Interpreter
from jsonmathpy.interfaces.interpreter_service import IInterpreterService
from jsonmathpy.models.basic_nodes import NodeConfigurationModel

class InterpreterService(IInterpreterService):
    """
     Implements ISerialiser.
    """
    def __init__(self, node):
        self.node = node
        self.interpreter_builder = InterpreterBuilder(
                                                        interpreter  = Interpreter,
                                                        node = self.node
                                                    )
        self.interpreter_instance = self.interpreter_builder.build()

    def interpret_ast_based_on_user_defined_config(self, string: str):
        return self.interpreter_instance.interpret(string)
