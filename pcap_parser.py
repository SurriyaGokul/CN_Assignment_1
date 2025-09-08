from scapy.all import PcapReader, DNS, DNSQR , Raw , wrpcap
import datetime

# function to count and store the DNS query packets
def pcap_parser(file):
    count=0
    dns_query_pkts=[]
    with PcapReader(file) as pcap_reader:
        for pkt in pcap_reader:
            if pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
                count+=1
                dns_query_pkts.append(pkt)
    return dns_query_pkts, count

# function to add custom header to each DNS query packet
def custom_header(pkt,id):
    new_pkt=pkt.copy()
    pkt_time = float(pkt.time) # used float as pkt.time is in EDecimal format
    timestamp = datetime.datetime.fromtimestamp(pkt_time)
    HH = f"{timestamp.hour:02d}"
    MM = f"{timestamp.minute:02d}"
    SS = f"{timestamp.second:02d}"
    ID = f"{id:02d}"
    header_str = HH + MM + SS + ID
    new_pkt = Raw(header_str.encode()) / new_pkt

    return new_pkt  

if __name__ == "__main__":
    file = "5.pcap"  
    dns_query_pkts, count = pcap_parser(file)
    print("Total DNS Queries:", count)
    header_added_pkts=[]
    id=0
    for pkt in dns_query_pkts:
        header_added_pkts.append(custom_header(pkt,id))
        id+=1
    for pkt in header_added_pkts:
        print(pkt.summary())
    wrpcap("dns_query_with_header.pcap", header_added_pkts)
    

