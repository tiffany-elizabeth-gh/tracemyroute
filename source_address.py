# This code will eventually be within trace_input not its own module
# add the optional user input for a starting IP address 
# this would allow the user to specify a specific starting point for the trace


import re


def source_address(source_ip):

    # pattern to validate the source IP address
    # only necessary for when source IP address is manually entered
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"


    if source_ip != "":
        # validate the source IP address, if entered manually
        if re.match(ip_pattern, source_ip):
            return True, source_ip
        else:
            return False, "Invalid source IP address. Please enter a valid IP address."
    else:
        # source ip is hardcoded for set up purposes
        # FUTURE add code to retrieve default source address rather than hardcode
        source_ip = "8.8.8.8"  # default source IP address
        print(f"Default source: {source_ip} is being used.") # printing source_ip for error checking
        return True, source_ip

#source = source_address()

if __name__ == "__main__":
    source_address("192.168.0.1") # hardcode some to be validated source here


# Future thoughts:
# Every computer has its own IP address and in order to run a traceroute from the individuals unique
# IP address, that IP address will need to be brought into this code
# For now, we have it hardcoded in
