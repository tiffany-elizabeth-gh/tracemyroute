'''Code to run a traceroute to a destination, identifying each hop's IP address'''


import subprocess
import socket
import requests
from ip2geotools.databases.noncommercial import DbIpCity
import geoip2.database



def trace_route(destination, max_hops=10):

    # get destination ip
    destination_ip = socket.gethostbyname(destination)

    # print traceroute command
    print(f"running traceroute on {destination} at {destination_ip}")

    # setting initial hop count
    hop_count = 0
    
    # create hop list for IP addresses
    hop_list = []

    # define traceroute
    traceroute = subprocess.Popen(["traceroute", destination], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    # identifying ip address for each hop en route to destination
    for line in iter(traceroute.stdout.readline, b""):
        line = line.decode("utf-8")
        IP_line = line.split(" ")
        if len(IP_line) > 1:
            for i, line in enumerate(IP_line):
                if line.startswith("("):
                    IP = next((line for line in IP_line if line.startswith("(")))
                    IP = IP.split("(")
                    if len(IP) > 1:
                        IP = IP[1].split(")")
                        IP = IP[0]
                        geo = DbIpCity.get(IP, api_key="free")
                        geolocation = (geo.city, geo.region, geo.country)
                        coordinates = (geo.latitude, geo.longitude)
                        hop_list.append({"hop": hop_count, "ip address": IP, "geolocation": geolocation, "coordinates": coordinates})
                        hop_count = hop_count + 1
                        print(hop_count, IP, geolocation)
                        break
            else:
                hop_list.append({"hop": hop_count, "ip address": "* * *", "geolocation": "N/A", "coordinates": "N/A"})
                hop_count = hop_count + 1
                print(hop_count, "* * *")
        if hop_count == max_hops+1:
            print("Max hops reached before destination was reached")
            break
    return f"Traceroute performed on {destination}"

if __name__ == "__main__":
    print(trace_route("www.walmart.com"))


# need to input code for error messages: unreachable host
# need to input code for max_hops reached

# first IP address in hop_list.append is the destination address - needs to be addressed for future
