import argparse
from scapy.all import *


def uncover_decoy_scans(pcap_file):
    pkts = rdpcap(pcap_file)

    scan_srcs = {}
    for pkt in pkts:
        if IP in pkt:
            src = pkt[IP].src
            if src in scan_srcs:
                scan_srcs[src] += 1
            else:
                scan_srcs[src] = 1

    decoy_scans = []
    for src in scan_srcs:
        if scan_srcs[src] > 1:
            decoy_scans.append(src)

    return decoy_scans


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uncover Decoy Network Scans")
    parser.add_argument("pcap_file", type=str, help="Name of the pcap file")
    args = parser.parse_args()

    try:
        decoy_scans = uncover_decoy_scans(args.pcap_file)
        print("Decoy Scans:")
        for decoy_scan in decoy_scans:
            print(decoy_scan)
    except Exception as e:
        print(f"Error: {e}")