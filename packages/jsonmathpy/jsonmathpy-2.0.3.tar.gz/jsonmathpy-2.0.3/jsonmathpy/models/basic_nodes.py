from dataclasses import dataclass


@dataclass
class NodeConfigurationModel:
    node_type: str
    node_handler: str