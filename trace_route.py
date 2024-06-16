# beginning to build the full trace_route module
# at this point this is where I am making notes 
# as I'm building the other elements so as not to forget


import re
import socket
import struct
import time
from scapy.all import *
import argparse




def trace_route(destination, source, max_hops=50, timeout=2):





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
