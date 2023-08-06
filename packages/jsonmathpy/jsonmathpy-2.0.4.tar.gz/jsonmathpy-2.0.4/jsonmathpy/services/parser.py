from jsonmathpy.builders.parser_builder import ParserBuilder
from jsonmathpy.core.iterator import Iterator
from jsonmathpy.core.lexer import Lexer
from jsonmathpy.core.parser import Parser
from jsonmathpy.core.token import TokenProvider
from jsonmathpy.core.nodes import NodeProvider
from jsonmathpy.interfaces.parser_service import IParserService
from jsonmathpy.models.node_keys import ConfigurationModels

class ParserService(IParserService):
    """
     Implements interface IParserService:
    """
    def __init__(self, node_configuration: ConfigurationModels):
        self.node_configuration = node_configuration
        self.parser_builder = ParserBuilder(
                                                        lexer               = Lexer, 
                                                        parser              = Parser, 
                                                        token_provider      = TokenProvider,
                                                        node_provider       = NodeProvider,
                                                        iterator            = Iterator,
                                                        configuration_models= self.node_configuration
                                                    )

    def get_ast(self, string: str):
        self.parser_instance = self.parser_builder.build(string)
        return self.parser_instance.parse()