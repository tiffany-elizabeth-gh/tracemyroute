# This code will eventually be within trace_input not its own module
# add the optional user input for a starting IP address 
# this would allow the user to specify a specific starting point for the trace


import re


def source_address(source_ip):

    # variables needed
    #source_ip = input("Enter the source IP address (leave blank for default): ")
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"  # pattern for IP address


    if source_ip != "":
        # validate the source IP address
        if re.match(ip_pattern, source_ip):
            return source_ip
        else:
            print("Invalid source IP address. Please enter a valid IP address.")
            return #????
    else:
        # source ip is hardcoded for set up purposes
        # FUTURE add code to retrieve default source address rather than hardcode
        source_ip = "8.8.8.8"  # default source IP address
        print(f"Default source: {source_ip} is being used.") # printing source_ip for error checking
        return source_ip

#source = source_address()

if __name__ == "__main__":
    source_address("192.168.0.1") # hardcode some to be validated source here
