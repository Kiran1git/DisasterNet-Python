import threading
import time
import uuid
from dataclasses import dataclass

from .config import NodeConfig
from .discovery import advertise_service, discover_peers
from .network import TCPServer, TCPClient


@dataclass
class DisasterNode:

    config: NodeConfig

    def __post_init__(self):
        self.node_id = f"node-{uuid.uuid4().hex[:6]}"
        self.running = False

        # mDNS
        self.zeroconf = None
        self.service_info = None
        self.peer_zeroconf = None
        self.peer_listener = None

        # TCP
        self.network = None

    def start(self):

        self.running = True

        print("=" * 35)
        print("       DisasterNet Python")
        print("=" * 35)

        print(f"Node ID   : {self.node_id}")
        print(f"Username  : {self.config.username}")
        print(f"Host      : {self.config.host}")
        print(f"Port      : {self.config.port}")

        # Start TCP server
        self.network = TCPServer(
            self.config.host,
            self.config.port,
            message_callback=self.receive_message
        )

        self.network.start()

        # Advertise this node
        self.zeroconf, self.service_info = advertise_service(
            self.node_id,
            self.config.port
        )

        # Discover peers
        (
            self.peer_zeroconf,
            self.peer_listener
        ) = discover_peers(
            self.node_id
        )

        print("Status    : ONLINE")
        print("\nWaiting for peers...")

        # Start command thread
        command_thread = threading.Thread(
            target=self.command_loop,
            daemon=True
        )

        command_thread.start()

        print("\nCommands:")
        print("  /peers")
        print("  /send <node_id> <message>")
        print("  /quit")

        try:

            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:

            self.stop()

    def command_loop(self):

        while self.running:

            try:

                command = input("\n> ").strip()

                if not command:
                    continue

                # Quit
                if command == "/quit":

                    self.stop()
                    break

                # Show peers
                elif command == "/peers":

                    self.show_peers()

                # Send message
                elif command.startswith("/send "):

                    parts = command.split(" ", 2)

                    if len(parts) < 3:

                        print(
                            "Usage: /send <node_id> <message>"
                        )

                        continue

                    target_node_id = parts[1]
                    message = parts[2]

                    self.send_message(
                        target_node_id,
                        message
                    )

                else:

                    print("Unknown command.")
                    print(
                        "Use /peers, /send, or /quit"
                    )

            except EOFError:

                self.stop()
                break

            except Exception as error:

                print(
                    f"[COMMAND ERROR] {error}"
                )

    def show_peers(self):

        if not self.peer_listener:

            print(
                "[ERROR] Peer discovery is not running."
            )

            return

        peers = self.peer_listener.peers

        if not peers:

            print("\nNo peers discovered.")
            return

        print("\n[PEERS]")

        for node_id, peer in peers.items():

            print(
                f"- {node_id} "
                f"({peer['ip']}:{peer['port']})"
            )

    def send_message(
        self,
        target_node_id,
        message
    ):

        if not self.peer_listener:

            print(
                "[ERROR] Peer discovery is not running."
            )

            return

        peer = self.peer_listener.peers.get(
            target_node_id
        )

        if not peer:

            print(
                f"[ERROR] Peer {target_node_id} not found."
            )

            return

        ip = peer["ip"]
        port = peer["port"]

        print(
            f"\n[SENDING] To {target_node_id}"
        )

        print(
            f"[NETWORK] Connecting to "
            f"{ip}:{port}"
        )

        TCPClient.send_message(
            ip,
            port,
            self.node_id,
            self.config.username,
            message
        )

    def receive_message(self, message_data):

        if message_data.get("type") != "chat":

            print(
                "\n[ERROR] Unknown message type."
            )

            return

        message_id = message_data.get(
            "message_id",
            "unknown"
        )

        sender_node_id = message_data.get(
            "sender_node_id",
            "unknown"
        )

        sender_username = message_data.get(
            "sender_username",
            "Unknown"
        )

        message = message_data.get(
            "message",
            ""
        )

        timestamp = message_data.get(
            "timestamp",
            "unknown"
        )

        print("\n" + "=" * 40)
        print("[NEW MESSAGE]")
        print(f"From       : {sender_username}")
        print(f"Node ID    : {sender_node_id}")
        print(f"Message    : {message}")
        print(f"Message ID : {message_id}")
        print(f"Time       : {timestamp}")
        print("=" * 40)

    def stop(self):

        if not self.running:
            return

        self.running = False

        # Stop peer discovery
        if self.peer_zeroconf:

            self.peer_zeroconf.close()

            self.peer_zeroconf = None
            self.peer_listener = None

        # Stop mDNS advertisement
        if self.zeroconf:

            self.zeroconf.unregister_all_services()
            self.zeroconf.close()

            self.zeroconf = None
            self.service_info = None

        # Stop TCP server
        if self.network:

            self.network.stop()

            self.network = None

        print("\nNode shutting down...")
        print("Status    : OFFLINE")