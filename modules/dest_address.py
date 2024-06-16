# Code that expands on trace_input to convert the given url to an IP address
# I brought the code in from trace_input to keep pieces separate for initial troubleshooting

# variables needed for this module
#destination = trace_input(destination)

import re
import socket
import struct
import time
from scapy.all import *
import argparse




def dest_address():

    destination = input("Enter a destination (URL/IP): ")

    # for converting a host to an ip
    destination_ip = socket.gethostbyname(destination)

    # port, ttl, and max_hops defaults
    max_hops = 50
    port = 33434 # this is a default starting port for UDP packets in traceroute
    ttl = 1

    # define qualifications for destination input
    url_pattern = r"((https?\:\/\/)?((?:www\.))?)[a-zA-Z]+[0-9]*\.([a-zA-Z]{2,3})((?:\.[a-zA-Z]{2}))?"
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"
    
    # check validitiy of input destination
    if destination != "":
        if re.match(url_pattern, destination):
            destination = destination_ip
            print("URL detected. Converting to IP...")
            while True:
                # create IP and UDP headers
                ip_packet = IP(dst=destination, ttl=ttl)
                udp_packet = UDP(dport=port)

                # combine headers
                packet = ip_packet / udp_packet

                # send packet and receive reply
                reply = srl(packet, timeout=timeout, verbose=0)

                # if loop to account for sent packet/reply
                if reply is None:
                    # no reply, print * for timeout
                    print(f"{ttl}\t*")
                elif reply.type == 3:
                    # destination reached, print details
                    print(f"{ttl}\t{reply.src}")
                    break
                else:
                    # print intermediate hop details
                    print(f"{ttl}\t{reply.src}")
                ttl += 1

                if ttl > max_hops:
                    break


        elif re.match(ip_pattern, destination):
            print("Valid IP")
        else:
            print("Invalid input. Please enter a valid URL or IP address.")
    else:
        print("Invalid input. Please enter a valid URL or IP address.")



# research parsing to see if that will be important to the overall traceroute