from dataclasses import dataclass
from typing import Any, Dict, List
from jsonmathpy.models.basic_nodes import NodeConfigurationModel
from jsonmathpy.models.node_handler import NodeHandler
from jsonmathpy.models.object_configuration import ObjectConfigurationModel

@dataclass
class ConfigurationModels:
    node_configurations: List[NodeConfigurationModel]
    objs_configurations: List[ObjectConfigurationModel]

    def get_node_handlers(self) -> dict[str, NodeHandler]:
        return { i.node_key : i.node_handler for i in self.node_configurations }