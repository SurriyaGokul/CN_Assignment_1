import socket 
from scapy.all import rdpcap, Raw

def send_packets(server_ip, server_port, pcap_file):
    packets = rdpcap(pcap_file)
    for pkt in packets:
        if Raw in pkt:
            raw_bytes = bytes(pkt[Raw])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            sock.connect((server_ip, server_port))
            sock.sendall(raw_bytes)
            print("Sent one packet")

            response = sock.recv(4096)
            print("Response:", response.decode(errors="ignore"))

            sock.close()    


if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 9090
    FILE = "dns_query_with_header.pcap"

    send_packets(SERVER_IP, SERVER_PORT, FILE)
