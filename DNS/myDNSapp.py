from scapy.all import *
"""""
from scapy.layers.dns import DNSQR
from scapy.layers.inet import UDP


def filterDNS(p)

p=DNS()
p= IP(dst="8.8.8.8")/UDP(dport=53)/DNS(qr=0, rd=1,qdcount=1,qd=[DNSQR](qname=b'www.youtube.com'))
r=sr1(p,verbose=0,timeout=2)  // אם הוא לא קיבל תשובה אז

if r is not None:
    print(r[DNSQR].qname)
x=DNSRR()
x.rdata  //
"""""



"""
def nslookup(domain):

    dns_request = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain, qtype="A"))
    response = sr1(dns_request, verbose=0, timeout=3)

    if response and response.haslayer(DNS):
        numOfAns=response[DNS].ancount
        for i in range(numOfAns):
            r=response[DNS].an[i]
            if r.type == 5:  # CNAME
                print("Canonical name:", r.rdata.decode())
            elif r.type == 1:
                print("IPv4:", r.rdata)
                h
                k
"""

