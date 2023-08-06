from jsonmathpy.interfaces.parser_service import IParserService
from jsonmathpy.interfaces.interpreter_service import IInterpreterService
from jsonmathpy.models.basic_nodes import NodeConfigurationModel

class JsonMathBuilder:

    def __init__(self, parser_service: IParserService, interpreter_service: IInterpreterService, node_configuration: NodeConfigurationModel, node):
        self.parser_service = parser_service
        self.interpreter_service = interpreter_service
        self.node_configuration = node_configuration
        self.node = node

    def interpreter_service_instance(self) -> IInterpreterService:
        return self.interpreter_service(self.node)

    def parser_service_instance(self) -> IParserService:
        return self.parser_service(self.node_configuration)
