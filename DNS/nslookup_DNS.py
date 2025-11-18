from scapy.all import *
from scapy.layers.dns import DNSQR

def nslookupPTR(IPorDOM, domainIP):
    dns_request=""
    if IPorDOM == 0:
        dns_request = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domainIP, qtype="A"))

    elif IPorDOM == 1:
        reversed_ip = ".".join(domainIP.split(".")[::-1]) + ".in-addr.arpa"
        dns_request = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=reversed_ip, qtype="PTR"))

    response = sr1(dns_request, verbose=0, timeout=5)

    if response and response.haslayer(DNS):
        numOfAns=response[DNS].ancount
        for i in range(numOfAns):
            r=response[DNS].an[i]
            if r.type == 5:  # CNAME
                print("Canonical name:", r.rdata.decode())
            elif r.type == 1:
                print("IPv4:", r.rdata)
            elif r.type == 12:
                print("Domain:", r.rdata.decode())


def main():
    IPorDOM= int(input("Domain to IP- Enter 0 \n" + "IP to Domain- Enter 1\n"))
    if IPorDOM == 0:
        domainIP = input("Enter Domain Name- \n")
    elif IPorDOM == 1:
        domainIP = input("Enter IP- \n")
    nslookupPTR(IPorDOM, domainIP)



if __name__ == "__main__":
    main()