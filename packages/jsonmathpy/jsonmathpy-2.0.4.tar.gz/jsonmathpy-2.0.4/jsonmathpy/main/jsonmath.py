from jsonmathpy.builders.jsonmath_builder import JsonMathBuilder
from jsonmathpy.main.base_node import DefaultNode, default_node_configuration
from jsonmathpy.services.parser import ParserService
from jsonmathpy.services.interpreter import InterpreterService
from jsonmathpy.models.basic_nodes import NodeConfigurationModel
from jsonmathpy.models.mapper import Mappers
from jsonmathpy.models.node_keys import ConfigurationModels
from jsonmathpy.models.object_configuration import ObjectConfigurationModel

class JsonMathPy:

    def __init__(self, node = DefaultNode(),  node_configuration: list = default_node_configuration, object_configuration : list = []):
        self.node = node
        self.node_configurations = ConfigurationModels(
                                                        Mappers.map_from_list(node_configuration, NodeConfigurationModel), 
                                                        Mappers.map_from_list(object_configuration, ObjectConfigurationModel)
                                                      )
        self.json_math_builder = JsonMathBuilder(
            ParserService,
            InterpreterService,
            self.node_configurations,
            self.node
        )
        self.parser_service = self.json_math_builder.parser_service_instance()
        self.interpreter_service = self.json_math_builder.interpreter_service_instance()

    def exe(self, expression: str):
        AST = self.parser_service.get_ast(expression)
        return self.interpreter_service.interpret_ast_based_on_user_defined_config(AST)

    def parse(self, string: str):
        return self.parser_service.get_ast(string)

    def iterpret(self, ast: dict):
        return self.interpreter_service.interpret_ast_based_on_user_defined_config(ast)
