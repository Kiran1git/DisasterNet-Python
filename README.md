# DisasterNet Python

A Python-based local-network emergency communication prototype inspired by DisasterNet.

## Features

- Unique node IDs
- mDNS peer discovery using Zeroconf
- TCP peer-to-peer communication
- Peer discovery using `/peers`
- Direct messaging using `/send`
- JSON-based message format
- Sender username and Node ID
- Unique message IDs
- Message timestamps

## Requirements

- Python 3.10+
- Devices connected to the same local network

## Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1