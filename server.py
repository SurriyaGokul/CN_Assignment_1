import socket
import json

with open("rules.json") as f:
    rules_config = json.load(f)

with open("config.json") as f:
    server_config = json.load(f)

HOST = server_config["host"]
PORT = server_config["port"]
ip_pool = rules_config["ip_pool"]
rules = rules_config["rules"]

def resolve_ip(custom_header):
    hour = int(custom_header[:2])   
    query_id = int(custom_header[6:])  
    
    if rules["morning"]["range"][0] <= hour <= rules["morning"]["range"][1]:
        pool_start = rules["morning"]["start"]
    elif rules["afternoon"]["range"][0] <= hour <= rules["afternoon"]["range"][1]:
        pool_start = rules["afternoon"]["start"]
    elif rules["night"]["range"][0] <= hour <= rules["night"]["range"][1] or \
         rules["extra_night"]["range"][0] <= hour <= rules["extra_night"]["range"][1]:
        pool_start = rules["night"]["start"]
    else:
        pool_start = 0  

    offset = query_id % 5
    index = pool_start + offset
    return ip_pool[index]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Server running (Just for checking lol)")

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(4096)
    if not data:
        break

    # Split header + dns query
    custom_header = data[:8].decode()
    dns_query = data[8:]  
    
    resolved_ip = resolve_ip(custom_header)
    print(f"Query received | Header: {custom_header} | Resolved IP: {resolved_ip}")
    
    response = custom_header.encode() + resolved_ip.encode()
    conn.sendall(response)
    conn.close()
