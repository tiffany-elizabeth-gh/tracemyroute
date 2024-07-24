''' source_address(source) is code to identify the source IP address for the traceroute.
The code includes the ability to validate a manually input IP address matched against an ip_pattern,
but is not included as a feature for a first release. More debugging has to occur before it is a fully
working feature. Error handling is included for future features.'''


import re
import socket


def source_address(source):

    # pattern to validate the source IP address
    # only necessary for when source IP address is manually entered
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"


    if source is True:
        # validate the source IP address, if entered manually
        if re.match(ip_pattern, source) is True:
            return f"Source IP is {source}"
        else:
            return False, f"Invalid source IP address {source}. Please enter a valid IP address or leave blank for default source IP."
    else:
        # code to retrieve user's IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        source = local_ip
        #print(f"Your Computer IP Address is: {source}")    # for debugging

        return f"Source IP is {source}"

if __name__ == "__main__":
    result, message = source_address("192.168.0.1")
    print(message)

