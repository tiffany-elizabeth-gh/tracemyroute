# beginning to build the full trace_route module
# at this point this is where I am making notes 
# as I'm building the other elements so as not to forget


import re
import socket
import struct
import time
from scapy.all import *
import argparse

from source_address import source_ip
from dest_address import destination


def trace_route(destination, source, max_hops=50, timeout=2):
    
    # defining variabls
    timeout = 2
    port = 33434
    ttl = 1
    ICMP = socket.getprotobyname('icmp')
    UDP = socket.getprotobyname('udp')

    # creating socket objects
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, UDP)

    timeout_struct = struct.pack('ll', timeout, 0)
    icmp_socket.bind(("", port)) # binds the ICMP protocol to the port
    icmp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout_struct)


    # defining the destination host
    destination_ip = socket.gethostbyname(destination) # NOTE this is for a url NOT an IP

    # for troubleshooting
    print(f"Tracerouting...{destination}({destination_ip})")

    while True:
        # creating the UDP packet
        udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        udp_socket.sendto(b'', (destination_ip, port))
        
        # setting start time
        start_time = time.time()
        no_tries = 3
        
        # defining Bool
        success = False
        done = False

        #
        while no_tries > 0:
            try:
                # receiving the ICMP packet
                packet, addr = icmp_socket.recvfrom(512)
                success = True
            except socket.error:
                no_tries -= 1
                continue
            if addr[0] == destination_ip:
                done = True
                break
        if success:
            end_time = time.time()
            try:
                name = socket.gethostbyaddr(addr[0])[0]
            except: pass
            t = round((end_time - start_time) * 1000, 4)
            print(f"TTL: {ttl} Addr: {name} ({addr[0]}) Time: {t}ms")
        else:
            print(f"TTL: {ttl} * * *")
        
        if done:
            break
        ttl += 1
    
    print("Traceroute completed.")


if __name__ == "__main__":
    trace_route("")


# placed the parsing function here for now
# needed for parsing through the traceroute details of a packet
# could be necessary for populating map with hop details

def main_parse():
    parser = argparse.ArgumentParser(description="Traceroute implementation in Python.")
    parser.add_argument("destination", help="Destination host or IP address.")
    parser.add_argument("source", help="Source IP address.")
    parser.add_argument("-m", "--max-hops", type=int, default=50, help="Maximum number of hops (default: 50).")
    parser.add_argument("-t", "--timeout", type=int, default=2, help="Timeout for each packet in seconds (default: 2).") # this may need future troubleshooting if this is too low

    args = parser.parse_args()

    print(f"Traceroute to {args.destination} (max hops: {args.max_hops}, timeout: {args.timeout} seconds):")
    trace_route(args.destination, args.source, max_hops=args.max_hops, timeout=args.timeout)

if __name__ == "__main__":
    main_parse()
