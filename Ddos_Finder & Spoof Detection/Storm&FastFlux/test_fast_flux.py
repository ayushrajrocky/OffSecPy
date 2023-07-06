from scapy.all import rdpcap
from scapy.layers.dns import DNSRR

dns_records = {}


def analyze_dns_records(pcap_file):
    pkts = rdpcap(pcap_file)

    for pkt in pkts:
        if DNSRR in pkt:
            rrname = pkt[DNSRR].rrname.decode('utf-8')
            rdata = pkt[DNSRR].rdata

            if rrname in dns_records:
                if rdata not in dns_records[rrname]:
                    dns_records[rrname].append(rdata)
            else:
                dns_records[rrname] = [rdata]

    return dns_records


if __name__ == "__main__":
    pcap_file = "fast_flux.pcap"  # Update with your pcap file path
    dns_records = analyze_dns_records(pcap_file)

    for rrname, ips in dns_records.items():
        unique_ips = len(ips)
        print(f"[+] {rrname} has {unique_ips} unique IPs.")
