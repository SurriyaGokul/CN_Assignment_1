import socket 
from scapy.all import rdpcap, Raw, DNS

def send_packets(server_ip, server_port, pcap_file):
    packets = rdpcap(pcap_file)
    
    for i, pkt in enumerate(packets):
        # take the raw bytes of the packet
        packet_bytes = bytes(pkt)
        
        # extracting custom header and DNS payload
        header = packet_bytes[:8].decode("ascii")  
        dns_payload = packet_bytes[8:]
        
        # to extract domain name from packet bytes
        try:
            query_name = "Unknown"
            # searching for DNS query pattern in the packet
            for pos in range(50, len(packet_bytes) - 10):
        
                if packet_bytes[pos] > 0 and packet_bytes[pos] < 64:  # byte length
                    try:
                        domain_parts = []
                        j = pos
                        while j < len(packet_bytes) and packet_bytes[j] != 0:
                            length = packet_bytes[j]
                            if length == 0 or length > 63 or j + length >= len(packet_bytes):
                                break
                            part = packet_bytes[j+1:j+1+length].decode('utf-8', errors='ignore')
                            # checking for a valid domain part (more inclusive for service names)
                            if part and all(c.isprintable() and c not in '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f' for c in part):
                                domain_parts.append(part)
                                j += length + 1
                            else:
                                break
                        
                        if len(domain_parts) >= 2:  # At least domain.tld
                            query_name = '.'.join(domain_parts)
                            break
                    except:
                        continue
        except:
            query_name = "Unknown"
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        
        sock.sendall(packet_bytes)
        
        response = sock.recv(4096)
        full_response = response.decode(errors="ignore").strip()
        
        # extracting IP address from response
        if len(full_response) > 8:
            resolved_ip = full_response[8:]  # ignore the initial header
        else:
            resolved_ip = full_response
        
        # for report format 
        print(f"Query {i+1}:")
        print(f"  Custom header value (HHMMSSID): {header}")
        print(f"  Domain name: {query_name}")
        print(f"  Resolved IP address: {resolved_ip}")
        print("-" * 50)
        
        sock.close()    


if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 9090
    FILE = "dns_query_with_header.pcap"

    send_packets(SERVER_IP, SERVER_PORT, FILE)