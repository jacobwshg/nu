#!/bin/python3.12

## import socket
from socket import socket, AF_INET, SOCK_DGRAM
from concurrent.futures import ThreadPoolExecutor as TPE
import os
import json
import threading 

LOCALHOST = "127.0.0.1"
LIS_PORT = 1053
UPSTREAM = "8.8.8.8"
FWD_PORT = 53
BUFSIZ = 2048

FWD_TIMEOUT = 3.0
FWD_MAX_RETRIES = 3

NTHREADS = os.cpu_count()

DNS_HDRLEN = 12

LOG_PATH = "dns-log.json"
LOG_LOCK = threading.Lock()

def set_cursor_blink():
    print("\033[?12;25h")

def get_query_name_and_type(query):
    qlen = len(query)
    if qlen < DNS_HDRLEN:
        print("Invalid query")
        return None, None

    labels = []

    # Advance byte position past header 
    # to leftmost label's length byte 
    pos = DNS_HDRLEN

    cur_byte = query[pos]
    while(cur_byte > 0):
        # Now CUR_BYTE holds label length
        label_len = cur_byte
        # Advance POS to initial byte in label
        pos += 1
        label = query[pos:(pos+label_len)].decode(encoding="ascii") 
        labels.append(label)
        # Advance POS to next label length or null-terminator
        pos += label_len
        cur_byte = query[pos]

    qname = ".".join(labels)

    # Now POS is at null-terminator past labels;
    # the following two bytes hold the query type 
    typeid = (query[pos+1] << 8) + query[pos+2]
    ### Debug
    ##print(f"typeid: {typeid} = 0x {query[pos+1]:0>2x} {query[pos+2]:0>2x}")
    qtype = ""
    match typeid:
        case 1:
            qtype = "A" 
        case 2:
            qtype = "NS"
        case 5:
            qtype = "CNAME"
        case 15:
            qtype = "MX"
        case 28:
            qtype = "AAAA"
        case _:
            qtype = "Other"

    return qname, qtype

class DNSProxy:
    def __init__(self):
        self.lis_addr = ( LOCALHOST, LIS_PORT )
        self.fwd_addr = ( UPSTREAM, FWD_PORT )
        self.lis_skt = None
        self.log = []

    def process_query(self, query, q_addr):
        qname, qtype = get_query_name_and_type(query)
        
        print(f"DNS query from {q_addr[0]}:{q_addr[1]}: QNAME {qname}, QTYPE {qtype}")

        resp = b""
        with socket(AF_INET, SOCK_DGRAM) as fwd_skt:
            fwd_skt.settimeout(FWD_TIMEOUT)

            for _attempt in range(FWD_MAX_RETRIES):
                try:
                    # Relay local query
                    fwd_skt.sendto(query, self.fwd_addr)
                    resp, _ = fwd_skt.recvfrom(BUFSIZ)
                except TimeoutError:
                    continue

            if len(resp) > 0:
                # Relay upstream response
                self.lis_skt.sendto(resp, q_addr)
            else:
                print("Upstream timed out")

        # Add log entry for current query and response
        logent =\
            {\
                "qname": qname,\
                "qtype": qtype,\
                "response_size": len(resp)\
            }
        with LOG_LOCK:
            self.log.append(logent)

    def run_server(self):
        with socket(AF_INET, SOCK_DGRAM) as self.lis_skt:
            self.lis_skt.bind(self.lis_addr)
            print(f"DNS proxy ready at localhost:{LIS_PORT}")
            set_cursor_blink()

            with TPE(max_workers=NTHREADS) as tpe:
                try:
                    while True:
                        query, q_addr = self.lis_skt.recvfrom(BUFSIZ)
                        tpe.submit(self.process_query(query, q_addr))
                except KeyboardInterrupt:
                    print("\nReceived keyboard interrupt.\nShutting down...")
                    tpe.shutdown(wait=True, cancel_futures=True)
                    # Log all queries and responses
                    with open(LOG_PATH, mode="w") as logfile:
                        json.dump(self.log, logfile, indent=4)
                    exit()
                
if __name__ == "__main__":
    pxy = DNSProxy()
    pxy.run_server()

