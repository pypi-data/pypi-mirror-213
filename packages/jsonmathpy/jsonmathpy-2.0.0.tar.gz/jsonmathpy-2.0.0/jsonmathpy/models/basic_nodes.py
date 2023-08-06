from dataclasses import dataclass


@dataclass
class NodeConfigurationModel:
    node: str
    node_key: str
    node_handler: object

    def __dict__(self):
        return { self.node_key : self.node_handler }