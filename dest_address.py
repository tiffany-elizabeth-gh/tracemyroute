''' dest_address(destination) is code to identify a destination address as URL or IP
If the destination is a URL, the url is validated and then converted to an IP address.
If the destination is an IP address, the IP address is validated.
If the destination is neither a URL or IP address or returns False, 
corresponding error messages will be outputted'''


import re
import socket


def dest_address(destination):

    # define qualifications for destination input
    url_pattern = r"((https?\:\/\/)?((?:www\.))?)[a-zA-Z]+[0-9]*\.([a-zA-Z]{2,3})((?:\.[a-zA-Z]{2}))?"
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"
    
    # check validity of input destination
    if destination is not None:
        if re.match(url_pattern, destination):
            #convert url to IP
            destination = socket.gethostbyname(destination)
            return True, f"Destination IP is {destination}"
        # if destination is not a URL, check if it is an IP address
        elif re.match(ip_pattern, destination):
            return True, f"Valid IP {destination}"
        else:
            return False, "Invalid input. Please enter a valid URL or IP address."
    # not a valid URL or IP address
    else:
        return False, "Invalid input. Please enter a valid URL or IP address."

if __name__ == "__main__":
    result, message = dest_address("www.google.com")
    print(message)