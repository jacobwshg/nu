#!/bin/python3.12

from socket import socket, AF_INET, SOCK_DGRAM
from concurrent.futures import ThreadPoolExecutor as TPE
import os
import requests
from dnslib import DNSRecord, QTYPE, RR, A, CNAME
import time

LOCALHOST = "127.0.0.1"
LIS_PORT = 1053
BUFSIZ = 2048

# DoH endpoint (Google)
DOH_URL = "https://dns.google/resolve"

NTHREADS = os.cpu_count()

def set_cursor_blink():
    print("\033[?12;25h")

class DNSProxy:
    def __init__(self):
        self.lis_addr = (LOCALHOST, LIS_PORT)
        self.lis_skt = None
        self.session = None

    def process_query(self, starttime, query, q_addr):
        """
        Handle a DNS-over-UDP query and forward via DNS-over-HTTPS.
        """
        try:
            # Parse query
            dns_req = DNSRecord.parse(query)
            q = dns_req.questions[0]
            qname = str(q.qname).rstrip(".")
            qtype = QTYPE[q.qtype]

            print(f"Query from {q_addr}: {qname} ({qtype})")

            # Send HTTPS request to Google DoH API
            params = {"name": qname, "type": qtype}
            r = self.session.get(DOH_URL, params=params, timeout=3)
            data = r.json()

            # Build DNS response (preserving ID and question)
            dns_resp = DNSRecord(dns_req.header)
            dns_resp.header.id = dns_req.header.id
            dns_resp.header.qr = 1   # Mark as response
            dns_resp.add_question(q)

            if "Answer" in data:
                for ans in data["Answer"]:
                    name = ans["name"]
                    atype = ans["type"]
                    ttl = ans.get("TTL", 300)
                    rdata = ans["data"]

                    if atype == 1:  # A record
                        dns_resp.add_answer(RR(name, QTYPE.A, rdata=A(rdata), ttl=ttl))
                    elif atype == 5:  # CNAME
                        dns_resp.add_answer(RR(name, QTYPE.CNAME, rdata=CNAME(rdata), ttl=ttl))

            resp_bytes = dns_resp.pack()

            # Send DNS UDP response back to the client
            self.lis_skt.sendto(resp_bytes, q_addr)

            print(f"Query e2e latency: {time.perf_counter() - starttime}")

        except Exception as e:
            print(f"Error handling query from {q_addr}: {e}")

    def run_server(self):
        """
        Listen for UDP DNS queries and handle them with a thread pool.
        """
        with socket(AF_INET, SOCK_DGRAM) as self.lis_skt:
            self.lis_skt.bind(self.lis_addr)
            print(f"DNS-over-HTTPS proxy running at {LOCALHOST}:{LIS_PORT}")
            set_cursor_blink()

            with requests.Session() as self.session:
                with TPE(max_workers=NTHREADS) as tpe:
                    try:
                        while True:
                            query, q_addr = self.lis_skt.recvfrom(BUFSIZ)
                            starttime = time.perf_counter()
                            tpe.submit(self.process_query, starttime, query, q_addr)
                    except KeyboardInterrupt:
                        print("\nReceived keyboard interrupt.\nShutting down...")
                        tpe.shutdown(wait=True, cancel_futures=True)
                        exit()

if __name__ == "__main__":
    proxy = DNSProxy()
    proxy.run_server()

