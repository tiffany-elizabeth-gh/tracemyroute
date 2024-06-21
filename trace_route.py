

import re
import socket 
import time
import os

from source_address import source_address
from dest_address import dest_address


def trace_route(destination, max_hops=10, timeout=2):
    
    # defining variables
    port = 33434
    ttl = 1

    # a list to store hop results
    hop_results = []

    while ttl <= max_hops:
        # creating a socket (UDP) for each TTL
        open_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # setting the TTL
        open_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        # set valid IP address
        destination_ip = socket.gethostbyname(destination)

        # send packet to the destination with current TTL
        open_sock.sendto(b'', (destination_ip, port))

        # get the current time
        start_time = time.time()

        # receive response (if any)
        open_sock.settimeout(1) # set timeout to 1 second
        try:
            response = open_sock.recvfrom(1024)
            if response:
                end_time = time.time()
                rtt = end_time - start_time
                ip_address = response[1][0]
            else:
                rtt = None
                ip_address = None
        except socket.timeout:
            rtt = None
            ip_address = None
            print("Timeout: no response from destination")

        # add results to hops_results list
        hop_results.append((ttl, ip_address, rtt))

        # close the socket
        open_sock.close()

        # increment ttl for next probe
        ttl += 1

        # if destination is reached, stop
        if ip_address == destination:
            break

    return hop_results


if __name__ == "__main__":
    dest_result = dest_address("www.iastate.edu")
    if dest_result[0]:
        destination = dest_result[1]
        if socket.inet_aton(destination):
            results = trace_route(destination)
            for hop, ip_address, rtt in results:
                print(f"Hop {hop}: {ip_address}")
        else:
            print("Invalid destination IP address:", destination)
    else:
        print("Error resolving destination IP address:", dest_result[1])
