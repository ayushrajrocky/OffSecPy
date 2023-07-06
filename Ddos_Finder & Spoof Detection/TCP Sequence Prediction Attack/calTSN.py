from scapy.all import send, sr1
from scapy.layers.inet import IP, TCP


def cal_TSN(tgt):
    seq_num = 0
    pre_num = 0
    diff_seq = 0

    for x in range(1, 5):
        if pre_num:
            pre_num = seq_num
        pkt = IP(dst=tgt) / TCP()
        ans = sr1(pkt, verbose=0)
        seq_num = ans.getlayer(TCP).seq
        diff_seq = seq_num - pre_num
        print(f'[+] TCP Seq Difference: {str(diff_seq)}')

    return seq_num + diff_seq

tgt= '45.33.32.156'
cal_TSN(tgt)
