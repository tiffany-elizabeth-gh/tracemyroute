'''Code to run a traceroute to a destination, identifying each hop's IP address'''


import subprocess
import socket
import ipinfo

access_token = input("enter ipinfo.io access token: ")
handler = ipinfo.getHandler(access_token)

def trace_route(destination, max_hops=30):

    # get destination ip
    destination_ip = socket.gethostbyname(destination)

    # print traceroute command
    print(f"running traceroute on {destination} at {destination_ip}")

    # setting initial hop count
    hop_count = 0
    
    # create hop list for IP addresses
    hop_list = []

    # define traceroute
    traceroute = subprocess.Popen(["traceroute", "-w", "10", destination], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT,
                                  text=True)
    first_line = True

    
    while True:
        # get output from traceroute
        output = traceroute.stdout.readline()
        if not output:
            break # no more output
        print(output.strip())
        if first_line:
            first_line = False
            continue

        hop = output.split()
        hop_count = hop_count + 1

        # error handling for unresponsive hops
        if output.endswith("*\n"):
            hop_list.append({"hop": hop_count, "ip address": "* * *"})
            max_hops -= 1
            if max_hops == 0:
                print("Max hops reached")
                break
        else: 
            # reviewing hop details
            for i, output in enumerate(hop):
                if output.startswith("("):
                    IP = output.split("(")
                    IP = IP[1].split(")")
                    IP = IP[0]
                    hop_details = handler.getDetails(IP)

                    # pulling out specific details
                    for i in enumerate(hop_details.all.items()):
                        if i[1][0] == "hostname":
                            hostname = i[1][1]
                            print("hostname:", hostname)
                        elif i[1][0] == "country":
                            country = i[1][1]
                            print("country:", country)
                        elif i[1][0] == "city":
                            city = i[1][1]
                            print("city:", city)
                        elif i[1][0] == "region":
                            region = i[1][1]
                            print("region:", region)
                        elif i[1][0] == "latitude":
                            lat = i[1][1]
                            print("latitude:", lat)
                        elif i[1][0] == "longitude":
                            long = i[1][1]
                            print("longitude:", long)

                    hop_list.append({"hop": hop_count, 
                                    "ip address": IP, 
                                    "hostname": hostname, 
                                    "city": city, 
                                    "region": region,
                                    "country": country,
                                    "latitude": lat,
                                    "longitude":long})
        

    print(f"Final destination ({destination}) reached: {destination_ip}")
    
    return hop_list



if __name__ == "__main__":
    print(trace_route("www.airbnb.com"))



# hop count is off..
# did not implement max_hops + hop_count feature here yet
# source IP address has not been handled here

# OPTIONAL: add code for blocked countries