import sys
from pathlib import Path

# Add the project root to Python's import path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import NodeConfig
from app.node import DisasterNode


def test_node_creation():
    config = NodeConfig(
        username="Kiran",
        port=9000
    )

    node = DisasterNode(config)

    assert node.config.username == "Kiran"
    assert node.config.port == 9000
    assert node.node_id.startswith("node-")
    assert node.running is False


def test_node_start():
    config = NodeConfig(
        username="Kiran",
        port=9000
    )

    node = DisasterNode(config)

    node.running = True

    assert node.running is True


def test_node_stop():
    config = NodeConfig(
        username="Kiran",
        port=9000
    )

    node = DisasterNode(config)

    node.running = True

    node.stop()

    assert node.running is False