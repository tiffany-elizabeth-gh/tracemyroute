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
        #print(output.strip())
        
        # skip anything starting with traceroute as not hop
        if output.startswith("traceroute"):
            continue

        hop = output.split()
        hop_count = hop_count + 1

        # error handling for unresponsive hops
        if output.endswith("*\n"):
            hop_list.append({"ip": "* * *", "hostname": "N/A", "country": "N/A", 
                             "city": "N/A", "region": "N/A", "latitude": "N/A", "longitude": "N/A"})
            max_hops -= 1
            if max_hops == 0:
                print("Max hops reached")
                break
        else: 
            # reviewing hop details
            # true hop will be like this:
            # 1 routera-10-33-148-0.tele.iastate.edu (10.33.149.252) 5.385 ms 3.530 ms 3.521 ms
            for tok in output.split():
                if tok.endswith(")"): # find token ending in )
                    ip = tok[1:-1] # remove ()s
                    break
            else:
                continue 

            #print(ip) # for debugging

            hop_details = handler.getDetails(ip)
            #print(hop_details.all) # for debugging

            hop_dict = {}
            for key in ["ip", "hostname", "country", "city", "region", "latitude", "longitude"]:
                if key in hop_details.all:
                    hop_dict[key] = hop_details.all[key]
                else:
                    hop_dict[key] = "N/A"
            print(hop_dict)

            hop_list.append(hop_dict)
        

    print(f"Final destination ({destination}) reached: {destination_ip}")
    
    return hop_list



if __name__ == "__main__":
    print(trace_route("www.airbnb.com"))



# hop count is off..
# did not implement max_hops + hop_count feature here yet
# source IP address has not been handled here

# OPTIONAL: add code for blocked countries