# building the main code all together

#from validate_trace_ip import trace_import
#destination = input("Enter a destination (URL/IP): ")
#valid_dest = validate_trace_ip(destination)

import argparse
import os
import re
import requests
from scapy.all import *
import socket
import struct
import time


# defining the source address
def source_address(source_ip):

    # variables needed
    source_ip = input("Enter the source IP address (leave blank for default): ")
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"  # pattern for IP address


    if source_ip != "":
        # validate the source IP address
        if re.match(ip_pattern, source_ip):
            return source_ip
        else:
            print("Invalid source IP address. Please enter a valid IP address.")
    else:
        # source ip is hardcoded for set up purposes
        # FUTURE add code to retrieve default source address rather than hardcode
        source_ip = "8.8.8.8"  # default source IP address
        print(f"Default source: {source_ip} is being used.") # printing source_ip for error checking
        return source_ip

#source = source_address()

if __name__ == "__main__":
    source_address("")

# defining and validating the destination address
def validate_trace_ip(destination):
    
    # user initiates trace by entering a destination
    # the destination is either a URL/website or IP address
    destination = input("Enter a destination (URL/IP): ")

    # define qualifications for destination input
    url_pattern = r"((https?\:\/\/)?((?:www\.))?)[a-zA-Z]+[0-9]*\.([a-zA-Z]{2,3})((?:\.[a-zA-Z]{2}))?"
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"
    
    # check validitiy of input destination
    if destination != "":
        if re.match(url_pattern, destination):
            # convert URL to IP address
            destination_ip = socket.gethostbyname(destination) 

            # NOTE add error message here for exceptions

            return True, "Valid URL"
        elif re.match(ip_pattern, destination):
            # this is to differentiate between a url that needs to be converted at traceroute or an IP addr that doesn't
            destination_ip = destination
            return True, "Valid IP"
        else:
            return False, "Invalid input. Please enter a valid URL or IP address."
    else:
        return False, "Invalid input. Please enter a valid URL or IP address."
    

while True:
    destination = input("Enter a destination (URL/IP): ")
    result, err_str = validate_trace_ip(destination)

    if result == False:
        print(err_str, "try again!")
    else:
        break



if __name__ == "__main__":
    validate_trace_ip("")

# running a traceroute with the validated destination address
def trace_route(destination_ip, source_ip, max_hops=50, timeout=2):
    
    # defining variables
    
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

        # running a traceroute using the ICMP packet request/reply
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
