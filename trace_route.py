'''Code to run a traceroute to a destination, identifying each hop's IP address'''


import subprocess

def trace_route(destination):
    print(f"running traceroute on {destination}") # currently using this for debugging since the computation causes a slow output
    traceroute = subprocess.Popen(["traceroute", destination], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    hop_list = []
    for line in iter(traceroute.stdout.readline, b""):
        line = line.decode("utf-8")
        IP = line.split(" ")
        if len(IP) > 1:
            IP = IP[4].split("(")
            if len(IP) > 1:
                IP = IP[1].split(")")
                hop_list.append(IP[0])
                print(IP[0]) # currently using this for debugging since the computation causes a slow output
    return hop_list

if __name__ == "__main__":
    trace_route("www.walmart.com")


# debugging is showing minimal errors but still having trouble with the output
# need to input code for error messages: unreachable host
# need to input code for max_hops reached
