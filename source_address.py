''' source_address(source) is code to identify the source IP address for the traceroute.
If the source is entered manually, the IP address is validated. If the manually entered source IP
address is invalid, corresponding error message will be given.
If the source is not entered manually, the default source address will be used.'''


import re
import socket
import requests


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
        print(f"Your Computer IP Address is: {source}")

        return f"Source IP is {source}"

if __name__ == "__main__":
    result, message = source_address("192.168.0.1")
    print(message)

