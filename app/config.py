from dataclasses import dataclass


@dataclass
class NodeConfig:
    username: str
    host: str = "0.0.0.0"
    port: int = 9000