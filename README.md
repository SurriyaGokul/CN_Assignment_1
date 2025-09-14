# DNS Query Resolver

This repository contains a project that processes DNS query packets, adds custom headers, sends them to a server, and resolves IP addresses based on predefined rules. The project is implemented in Python and uses the `scapy` library for packet manipulation and `socket` library for TCP connections.

---

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [Configuration Files](#configuration-files)
- [How It Works](#how-it-works)
- [Example Output](#example-output)
- [Dependencies](#dependencies)

---

## **Overview**
This project simulates a DNS query resolver system. It consists of three main components:
1. **Packet Parser**: Reads DNS query packets from a `.pcap` file, adds custom headers, and saves the modified packets.
2. **Client**: Sends the modified packets to a server and displays the resolved IP addresses.
3. **Server**: Resolves IP addresses based on the custom header and predefined rules.

---

## **Features**
- Parses DNS query packets from `.pcap` files.
- Adds custom headers to packets with timestamp and unique IDs.
- Resolves IP addresses based on time ranges and rules.
- Simulates client-server communication using TCP sockets.

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.8 or higher
- `pip` (Python package manager)
- Install the required Python libraries:
  ```bash
  pip install scapy 
  ```

### **2. Clone the Repository**
```bash
git clone https://github.com/SurriyaGokul/CN_Assignment_1.git
cd CN_Assignment_1
```

---

## **How to Run**

### **Step 1: Parse the Packets**
Run the `pcap_parser.py` script to parse the input `.pcap` file and add custom headers:
```bash
python3 pcap_parser.py
```
This will generate a new `.pcap` file (`dns_query_with_header.pcap`) with custom headers.

### **Step 2: Start the Server**
Run the `server.py` script to start the server:
```bash
python3 server.py
```
The server will listen on the host and port specified in `config.json`.

### **Step 3: Run the Client**
Run the `client.py` script to send packets to the server:
```bash
python3 client.py
```
The client will send the packets from `dns_query_with_header.pcap` to the server and display the resolved IP addresses.

---

## **Configuration Files**

### **1. `config.json`**
Specifies the server's host and port:
```json
{
  "host": "127.0.0.1",
  "port": 9090
}
```

### **2. `rules.json`**
Defines the IP pool and rules for resolving IP addresses:
```json
{
  "ip_pool": [
    "192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5",
    "192.168.1.6", "192.168.1.7", "192.168.1.8", "192.168.1.9", "192.168.1.10",
    "192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14", "192.168.1.15"
  ],
  "rules": {
    "morning": { "range": [4, 11], "start": 0 },
    "afternoon": { "range": [12, 19], "start": 5 },
    "night": { "range": [20, 23], "start": 10 },
    "extra_night": { "range": [0, 3], "start": 10 }
  }
}
```

---

## **How It Works**

1. **Packet Parsing:**
   - The `pcap_parser.py` script reads DNS query packets from `5.pcap`.
   - Adds a custom header (timestamp + unique ID) to each packet.
   - Saves the modified packets to `dns_query_with_header.pcap`.

2. **Client-Server Communication:**
   - The `client.py` script reads packets from `dns_query_with_header.pcap`.
   - Sends each packet to the server via a TCP socket using the `socket` library.
   - Displays the resolved IP address received from the server.

3. **IP Resolution:**
   - The `server.py` script resolves IP addresses based on the custom header and rules defined in `rules.json`.
   - Sends the resolved IP address back to the client using the `socket` library for communication.

---

## **Example Output**

### **Client Output:**
```
Query 1:
  Custom header value (HHMMSSID): 12010100
  Domain name: example.com
  Resolved IP address: 192.168.1.1
```

### **Server Output:**
```
Server running (Just for checking lol)
Query received | Header: 12010100 | Resolved IP: 192.168.1.1
```

---

## **Dependencies**
- Python 3.8+
- `scapy` library
- `socket` library (built-in)

Install dependencies using:
```bash
pip install scapy
```