# DisasterNet Python

A Python-based local-network emergency communication prototype.

DisasterNet Python allows multiple nodes connected to the same local network to automatically discover each other and exchange messages directly using TCP.

# Features

- Unique Node IDs
- Automatic peer discovery using mDNS
- Zeroconf-based service advertisement
- TCP peer-to-peer communication
- Direct messaging between discovered peers
- JSON-based message protocol
- Sender username and Node ID
- Unique Message ID for every message
- Message timestamps
- Command-line interface
- Unit testing using Pytest

##  Architecture

text
                 DisasterNet Python
                         │
                         ▼
                ┌─────────────────┐
                │  DisasterNode   │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       ┌──────────────┐      ┌──────────────┐
       │ mDNS /       │      │ TCP          │
       │ Zeroconf     │      │ Networking   │
       └──────┬───────┘      └──────┬───────┘
              │                     │
              ▼                     ▼
       Peer Discovery          Message Exchange


#Peer Discovery

Each DisasterNet node advertises itself on the local network using mDNS/Zeroconf.

The service type used by the project is:

text
_disasternet._tcp.local.


Other DisasterNet nodes listen for this service and automatically discover available peers.

# Communication

After discovering a peer, nodes communicate directly using TCP sockets.

Messages are exchanged using JSON.

Example message:

json
{
  "type": "chat",
  "message_id": "msg-e313229c",
  "sender_node_id": "node-123456",
  "sender_username": "Kiran",
  "message": "Hello Rahul",
  "timestamp": "2026-09-27T10:30:00"
}


# Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Zeroconf | mDNS peer discovery |
| TCP Sockets | Peer-to-peer communication |
| Typer | Command-line interface |
| Pytest | Unit testing |
| JSON | Message serialization |

# Project Structure

```text
DisasterNet-Python/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── node.py
│   ├── config.py
│   ├── discovery.py
│   └── network.py
│
├── tests/
│   └── test_node.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Components

#### `app/main.py`

Application entry point.

Starts a DisasterNet node using the provided username and port.

#### `app/node.py`

Contains the main `DisasterNode` class.

Responsible for:

- Starting and stopping the node
- Managing peer discovery
- Managing TCP networking
- Processing commands
- Sending messages
- Receiving messages

#### `app/discovery.py`

Handles local-network peer discovery using Zeroconf and mDNS.

Responsible for:

- Advertising the current node
- Discovering other DisasterNet nodes
- Maintaining the discovered peer list

#### `app/network.py`

Handles TCP communication.

Responsible for:

- Running the TCP server
- Accepting incoming connections
- Sending messages to peers
- Processing JSON messages

#### `app/config.py`

Contains configuration information for a DisasterNet node.

#### `tests/test_node.py`

Contains unit tests for node creation and node lifecycle behavior.

## ⚙️ Requirements

- Python 3.10 or higher
- Devices connected to the same local network

# Installation

Clone the repository:

```bash
git clone https://github.com/Kiran1git/DisasterNet-Python.git
```

Move into the project directory:

```bash
cd DisasterNet-Python
```

Create a virtual environment:

# Windows

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

# Running the Application

#Start Node 1

Open a terminal:

powershell
python -m app.main Kiran --port 9000


# Start Node 2

Open another terminal:

powershell
python -m app.main Rahul --port 9001


Both nodes should be connected to the same local network.

The nodes will automatically discover each other.

# Available Commands

#View discovered peers

```text
/peers
```

Example:

```text
[PEERS]
- node-62988e (192.168.29.179:9001)
```

### Send a message

```text
/send <node_id> <message>
```

Example:

```text
/send node-62988e Hello Rahul
```

### Exit the application

```text
/quit
```

## 📡 Example

When a node starts, it displays information similar to:

```text
===================================
       DisasterNet Python
===================================

Node ID   : node-6f1bf7
Username  : Kiran
Host      : 0.0.0.0
Port      : 9000

[NETWORK] TCP server listening on port 9000

[DISCOVERY]
Node ID : node-6f1bf7
IP      : 192.168.29.179
Port    : 9000
Status  : ADVERTISED

Status    : ONLINE
```

After another node is discovered:

```text
[PEER DISCOVERED]
Node ID : node-62988e
IP      : 192.168.29.179
Port    : 9001
```

View the available peers:

```text
/peers
```

Output:

```text
[PEERS]
- node-62988e (192.168.29.179:9001)
```

Send a message:

```text
/send node-62988e Hello Rahul
```

The message contains:

```text
Message ID
Sender Node ID
Sender Username
Message
Timestamp
```

## 🧪 Testing

The project uses Pytest for unit testing.

Run:

```powershell
pytest
```

Expected result:

```text
3 passed
```

The current tests verify:

- Node creation
- Node configuration
- Node ID generation
- Node running state
- Node shutdown behavior

## 🔐 Current Scope

The current version focuses on:

- Local-network peer discovery
- Direct TCP communication
- Basic structured messaging
- Command-line interaction

The current implementation does **not** include:

- End-to-end encryption
- Message persistence
- Offline message storage
- Store-and-forward messaging
- Graphical user interface
- Internet-based communication

## 🔮 Future Improvements

Possible future improvements include:

- End-to-end message encryption
- Message history and persistence
- Offline message queuing
- Store-and-forward communication
- Chat rooms
- Web-based interface
- Improved peer management
- Network resilience
- File sharing
- Mobile support

## 📌 Project Status

**Working Prototype**

The current implementation successfully supports local-network peer discovery and direct TCP messaging between DisasterNet Python nodes.

## 📄 License

This project is currently provided for educational and development purposes.
