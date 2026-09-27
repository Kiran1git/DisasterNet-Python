import typer

from .config import NodeConfig
from .node import DisasterNode


def main(
    username: str,
    port: int = 9000
):
    config = NodeConfig(
        username=username,
        port=port
    )

    node = DisasterNode(config)

    # Start the node
    node.start()


if __name__ == "__main__":
    typer.run(main)