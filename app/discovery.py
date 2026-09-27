import socket

from zeroconf import (
    ServiceBrowser,
    ServiceInfo,
    ServiceListener,
    Zeroconf,
)


SERVICE_TYPE = "_disasternet._tcp.local."


def get_local_ip():


    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]

    finally:
        sock.close()


def advertise_service(node_id, port):
   

    zeroconf = Zeroconf()

    local_ip = get_local_ip()

    service_info = ServiceInfo(
        type_=SERVICE_TYPE,
        name=f"{node_id}.{SERVICE_TYPE}",
        addresses=[
            socket.inet_aton(local_ip)
        ],
        port=port,
        properties={
            "node_id": node_id
        },
        server=f"{node_id}.local.",
    )

    try:
        zeroconf.register_service(
            service_info
        )

    except Exception:
        zeroconf.close()
        raise

    print("\n[DISCOVERY]")
    print(f"Node ID : {node_id}")
    print(f"IP      : {local_ip}")
    print(f"Port    : {port}")
    print("Status  : ADVERTISED")

    return zeroconf, service_info


class PeerListener(ServiceListener):
   

    def __init__(self, own_node_id):

        self.own_node_id = own_node_id

        self.peers = {}

    def add_service(
        self,
        zeroconf,
        service_type,
        name
    ):
        """Called when a new peer is discovered."""

       
        if name == f"{self.own_node_id}.{SERVICE_TYPE}":
            return

        info = zeroconf.get_service_info(
            service_type,
            name
        )

        if not info:
            return

        addresses = info.parsed_addresses()

        if not addresses:
            return

        ip = addresses[0]

        node_id = info.properties.get(
            b"node_id",
            b"unknown"
        ).decode("utf-8")

      
        self.peers[node_id] = {
            "ip": ip,
            "port": info.port,
            "name": name
        }

        print("\n[PEER DISCOVERED]")
        print(f"Node ID : {node_id}")
        print(f"IP      : {ip}")
        print(f"Port    : {info.port}")

    def remove_service(
        self,
        zeroconf,
        service_type,
        name
    ):

        node_to_remove = None

        for node_id, peer in self.peers.items():

            if peer["name"] == name:
                node_to_remove = node_id
                break

        if node_to_remove:
            del self.peers[node_to_remove]

            print(
                f"\n[PEER LEFT] {node_to_remove}"
            )

        else:
            print(
                f"\n[PEER LEFT] {name}"
            )

    def update_service(
        self,
        zeroconf,
        service_type,
        name
    ):
       

        self.add_service(
            zeroconf,
            service_type,
            name
        )


def discover_peers(own_node_id):


    zeroconf = Zeroconf()

    listener = PeerListener(
        own_node_id
    )

    ServiceBrowser(
        zeroconf,
        SERVICE_TYPE,
        listener
    )

    return zeroconf, listener
