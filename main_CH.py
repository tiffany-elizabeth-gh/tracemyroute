# building the main code all together
import argparse
import os
import re
import requests
from scapy.all import *
import socket
import struct
import time

from validate_trace_ip import  validate_trace_ip
from source_address import source_address
from trace_route import trace_route

'''
# get source and destination, etc. from args
parser = argparse.ArgumentParser(description="Traceroute implementation in Python.")
parser.add_argument("destination", help="Destination host or IP address.")
parser.add_argument("source", help="Source IP address.")
parser.add_argument("-m", "--max-hops", type=int, default=50, help="Maximum number of hops (default: 50).")
parser.add_argument("-t", "--timeout", type=int, default=2, help="Timeout for each packet in seconds (default: 2).") # this may need future troubleshooting if this is too low
args = parser.parse_args()
'''

destination = source = max_hops = timeout = None    

# hardcode defaults, comment out for manual input!
destination = "www.google.com"
#source = "192.68.0.1"
max_hops = 50
timeout = 2


if not source:
    source = input("Enter a source (URL/IP): ")
source_ip = source_address(source)
print("Source IP: ", source_ip)


if not destination:
    while True:
        destination = input("Enter destination (URL/IP): ")
        result, err_str = validate_trace_ip(destination)

        if result == False:
            print(err_str, "try again!")
        else:
            break
    print("Valiated Destination: ", destination)

if not destination:
    while True:
        destination = input("Enter destination (URL/IP): ")
        result, err_str = dest_address(destination, max_hops=50, timeout=2)

        if result == False:
                print(err_str, "try again!")
        else:
            break
    print("Valiated Destination: ", destination)
    

# run trace_route()
print(f"Traceroute from {source} to {destination} (max hops: {max_hops}, timeout: {timeout} seconds):")
trace_route(destination, source, max_hops=max_hops, timeout=timeout)






