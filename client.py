import socket 
from scapy.all import rdpcap

def extract_domain_name(packet_bytes):
    try:
        # skip the 8-byte custom header first
        data_after_header = packet_bytes[8:]
        
        # looking for DNS query pattern in the data
        for offset in range(len(data_after_header) - 20):
            try:
                dns_data = data_after_header[offset:]
                
                # Skip DNS header (12 bytes) to get to the question section
                if len(dns_data) < 12:
                    continue
                    
                dns_question = dns_data[12:]
                
                # Parse domain name
                domain_parts = []
                i = 0
                
                while i < len(dns_question):
                    length = dns_question[i]
                    if length == 0:  # End of domain name
                        break
                    if length > 63 or length < 1:  # Invalid length
                        break
                    
                    i += 1
                    if i + length > len(dns_question):
                        break
                    
                    try:
                        label = dns_question[i:i+length].decode("ascii")
                        # Validate that the label contains only valid domain characters
                        if all(c.isalnum() or c == '-' for c in label) and len(label) > 0:
                            domain_parts.append(label)
                            i += length
                        else:
                            break  # Invalid character found
                    except:
                        break  # Decode failed
                
                if len(domain_parts) >= 2:  # Valid domain (at least domain.tld)
                    domain_name = ".".join(domain_parts)
                    return domain_name
                        
            except:
                continue
                
        return "Unknown"
    except:
        return "Unknown"

def send_packets(server_ip, server_port, pcap_file):
    packets = rdpcap(pcap_file)
    
    for i, pkt in enumerate(packets):
        # take the raw bytes of the packet
        packet_bytes = bytes(pkt)
        
        # extracting custom header and DNS payload
        header = packet_bytes[:8].decode("ascii")  
        query_name = extract_domain_name(packet_bytes)
        
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
        
        sock.close()    

if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 9090
    FILE = "dns_query_with_header.pcap"

    send_packets(SERVER_IP, SERVER_PORT, FILE)