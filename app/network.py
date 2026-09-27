import json
import socket
import threading
import uuid
from datetime import datetime


class TCPServer:

    def __init__(self, host, port, message_callback=None):
        self.host = host
        self.port = port
        self.running = False
        self.server_socket = None
        self.message_callback = message_callback

    def start(self):

        self.running = True

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.server_socket.bind(
            (self.host, self.port)
        )

        self.server_socket.listen(10)

        print(
            f"[NETWORK] TCP server listening on port {self.port}"
        )

        thread = threading.Thread(
            target=self._accept_connections,
            daemon=True
        )

        thread.start()

    def _accept_connections(self):

        while self.running:

            try:

                client_socket, address = (
                    self.server_socket.accept()
                )

                print(
                    f"\n[CONNECTION] Peer connected: {address}"
                )

                thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True
                )

                thread.start()

            except OSError:
                break

    def _handle_client(self, client_socket):

        try:

            data = client_socket.recv(4096)

            if not data:
                return

            message_data = json.loads(
                data.decode("utf-8")
            )

            if self.message_callback:

                self.message_callback(
                    message_data
                )

        except json.JSONDecodeError:

            print(
                "[ERROR] Received invalid message format."
            )

        except Exception as error:

            print(
                f"[NETWORK ERROR] {error}"
            )

        finally:

            client_socket.close()

    def stop(self):

        self.running = False

        if self.server_socket:

            try:
                self.server_socket.close()
            except OSError:
                pass

        print("[NETWORK] TCP server stopped")


class TCPClient:

    @staticmethod
    def send_message(
        host,
        port,
        sender_node_id,
        sender_username,
        message
    ):

        # Generate a unique message ID
        message_id = f"msg-{uuid.uuid4().hex[:8]}"

        # Get current UTC timestamp
        timestamp = datetime.utcnow().isoformat()

        message_data = {
            "type": "chat",
            "message_id": message_id,
            "sender_node_id": sender_node_id,
            "sender_username": sender_username,
            "message": message,
            "timestamp": timestamp
        }

        data = json.dumps(
            message_data
        ).encode("utf-8")

        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:

            client_socket.connect(
                (host, port)
            )

            client_socket.sendall(data)

            print(
                f"[NETWORK] Message sent to "
                f"{host}:{port}"
            )

            print(
                f"[NETWORK] Message ID: "
                f"{message_id}"
            )

        finally:

            client_socket.close()