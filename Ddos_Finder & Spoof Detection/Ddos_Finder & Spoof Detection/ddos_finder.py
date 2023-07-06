from scapy.all import *
import argparse


def find_attack(pcap):
    pkt_count = {}

    for packet in pcap:
        if not packet.haslayer(TCP):
            continue

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        dport = packet[TCP].dport

        if dport == 80:
            stream = f"{src_ip}:{dst_ip}"
            if stream in pkt_count:
                pkt_count[stream] += 1
            else:
                pkt_count[stream] = 1

    for stream, pkts_sent in pkt_count.items():
        if pkts_sent > THRESH:
            src_ip, dst_ip = stream.split(":")
            print(f"[+] {src_ip} attacked {dst_ip} with {str(pkts_sent)} packets.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ddosfind.py PCAP_FILE [-t THRESH]")
    parser.add_argument(
        "pcap_file",
        type=str,
        metavar="PCAP_FILE",
        help="specify the name of the pcap file",
    )
    parser.add_argument(
        "-t", type=int, metavar="THRESH", default=1000, help="specify threshold count"
    )

    args = parser.parse_args()
    pcap_file = args.pcap_file
    THRESH = args.t

    pcap = rdpcap(pcap_file)
    find_attack(pcap)