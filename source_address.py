''' source_address(source) is code to identify the source IP address for the traceroute.
If the source is entered manually, the IP address is validated. If the manually entered source IP
address is invalid, corresponding error message will be given.
If the source is not entered manually, the default source address will be used.'''


import re


def source_address(source):

    # pattern to validate the source IP address
    # only necessary for when source IP address is manually entered
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"


    if source is not None:
        # validate the source IP address, if entered manually
        if re.match(ip_pattern, source):
            return True, f"Source IP is {source}"
        else:
            return False, f"Invalid source IP address {source}. Please enter a valid IP address or leave blank for default source IP."
    else:
        # source ip is hardcoded for set up purposes
        # FUTURE add code to retrieve default source address rather than hardcode
        source = "8.8.8.8"  # default source IP address
        return True, f"Source IP is {source}"

if __name__ == "__main__":
    result, message = source_address("192.168.0.1")
    print(message)


# Future thoughts:
# Every computer has its own IP address and in order to run a traceroute from the individuals unique
# IP address, that IP address will need to be brought into this code
# For now, we have it hardcoded in
