# Time-Based DNS Resolution Server

A Python-based TCP server implementation that provides dynamic IP address resolution based on time-of-day routing rules. This server simulates a DNS-like service with custom header processing and intelligent IP pool management.

## 🌟 Features

- **Time-Based Routing**: Dynamically assigns IP addresses from different pools based on the current hour
- **Custom Protocol**: Handles queries with 8-byte custom headers containing timestamp and query ID
- **Configurable IP Pools**: Supports multiple IP address pools for different time periods
- **JSON Configuration**: Easy-to-modify configuration files for server settings and routing rules
- **Concurrent Connections**: Handles multiple client connections with proper socket management

## 🏗️ Architecture

The server consists of four main components:

### Core Files

| File | Purpose |
|------|---------|
| `server.py` | Main server implementation with TCP socket handling and IP resolution logic |
| `config.json` | Server configuration (host, port, IP pools) |
| `rules.json` | Time-based routing rules and IP pool assignments |
| `README.md` | Project documentation |

### Server Architecture

```
Client Request → Custom Header Processing → Time-Based Rule Evaluation → IP Pool Selection → Response
```

## 📋 Prerequisites

- Python 3.6 or higher
- Network connectivity for TCP socket operations
- Read access to configuration files (`config.json`, `rules.json`)

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SurriyaGokul/CN_Assignment_1.git
   cd CN_Assignment_1
   ```

2. **Verify Python installation**:
   ```bash
   python3 --version
   ```

3. **Ensure configuration files are present**:
   ```bash
   ls -la config.json rules.json server.py
   ```

## ⚙️ Configuration

### Server Configuration (`config.json`)

```json
{
  "host": "127.0.0.1",
  "port": 9090
}
```

- `host`: Server bind address (default: localhost)
- `port`: Server listening port (default: 9090)

### Routing Rules (`rules.json`)

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

#### Time Period Definitions

| Period | Hours (24h format) | IP Pool Range | Pool Start Index |
|--------|-------------------|---------------|------------------|
| Morning | 04:00 - 11:59 | IPs 1-5 | 0 |
| Afternoon | 12:00 - 19:59 | IPs 6-10 | 5 |
| Night | 20:00 - 23:59 | IPs 11-15 | 10 |
| Extra Night | 00:00 - 03:59 | IPs 11-15 | 10 |

## 🖥️ Usage

### Starting the Server

```bash
python3 server.py
```

The server will start and display:
```
Server running (Just for checking lol)
```

### Client Communication Protocol

#### Request Format
- **Total Length**: Variable (minimum 8 bytes)
- **Header**: 8 bytes (`HHMMSSQQ`)
  - `HH`: Hour (00-23)
  - `MM`: Minute (00-59)  
  - `SS`: Second (00-59)
  - `QQ`: Query ID (00-99)
- **DNS Query**: Variable length (after header)

#### Response Format
- **Header Echo**: 8 bytes (same as request header)
- **Resolved IP**: Variable length string

### Example Client Interaction

```python
import socket

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# Send request: "14305501" + DNS query
# (14:30:55, Query ID: 01)
request = b"14305501example.com"
client.sendall(request)

# Receive response
response = client.recv(4096)
header = response[:8].decode()  # "14305501"
ip = response[8:].decode()      # e.g., "192.168.1.7"

client.close()
```

## 🔍 Algorithm Details

### IP Resolution Logic

1. **Header Parsing**: Extract hour and query ID from 8-byte header
2. **Time Period Detection**: Determine current time period (morning/afternoon/night/extra_night)
3. **Pool Selection**: Choose IP pool based on time period rules
4. **Offset Calculation**: `offset = query_id % 5`
5. **IP Selection**: `selected_ip = ip_pool[pool_start + offset]`

### Load Distribution

The modulo operation (`query_id % 5`) ensures even distribution across 5 IPs within each time period's pool, providing basic load balancing.

## 🧪 Testing

### Manual Testing

1. **Start the server**:
   ```bash
   python3 server.py
   ```

2. **Test with telnet** (in another terminal):
   ```bash
   echo -n "14305501test.com" | nc 127.0.0.1 9090
   ```

3. **Expected output**: Header echo + resolved IP address

### Automated Testing Script

```python
import socket
import time

def test_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 9090))
        
        # Test afternoon period with query ID 1
        test_header = "14305501"
        client.sendall(test_header.encode() + b"test.com")
        
        response = client.recv(4096)
        header = response[:8].decode()
        ip = response[8:].decode()
        
        print(f"Request Header: {test_header}")
        print(f"Response Header: {header}")
        print(f"Resolved IP: {ip}")
        
    finally:
        client.close()

if __name__ == "__main__":
    test_server()
```

## 🚨 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `ConnectionRefusedError` | Server not running | Start server with `python3 server.py` |
| `FileNotFoundError` | Missing config files | Ensure `config.json` and `rules.json` exist |
| `JSONDecodeError` | Invalid JSON syntax | Validate JSON format in config files |
| `Address already in use` | Port conflict | Change port in `config.json` or kill existing process |
| `Permission denied` | Insufficient privileges | Use ports > 1024 or run with appropriate permissions |

### Debug Information

The server logs each query with format:
```
Query received | Header: HHMMSSQQ | Resolved IP: X.X.X.X
```

## 🔧 Customization

### Adding New Time Periods

1. Modify `rules.json` to add new time ranges
2. Update IP pool assignments as needed
3. Restart the server

### Changing IP Pools

1. Edit the `ip_pool` array in `rules.json`
2. Adjust `start` indices in rules accordingly
3. Ensure pool ranges don't exceed available IPs

## 📊 Performance Considerations

- **Concurrent Connections**: Limited by system socket limits
- **Memory Usage**: Minimal - configuration loaded once at startup
- **CPU Usage**: O(1) IP resolution per query
- **Network Latency**: Dependent on client-server network conditions

## 🔒 Security Notes

- Server binds to localhost by default (127.0.0.1)
- No authentication or encryption implemented
- Suitable for development/testing environments
- For production use, consider adding TLS and authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of a Computer Networks assignment. Please refer to your institution's academic integrity policies.

## 📞 Support

For technical questions or issues:
- Review the troubleshooting section
- Check server logs for error messages
- Verify configuration file syntax
- Ensure network connectivity

---

**Author**: SurriyaGokul  
**Course**: Computer Networks Assignment 1  
**Last Updated**: 2024