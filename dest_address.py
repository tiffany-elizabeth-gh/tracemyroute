''' dest_address(destination) is code to identify a destination address as URL or IP
If the destination is a URL, the url is validated and then converted to an IP address.
If the destination is an IP address, the IP address is validated.
If the destination is neither a URL or IP address or returns False, 
corresponding error messages will be outputted'''


import re
import socket
from urllib import parse 


def dest_address(destination):
    '''Identify the destination IP address for tracemyroute'''
    # define qualifications for destination input
    #url_pattern = r"((https?\:\/\/)?((?:www\.))?)[a-zA-Z]+[0-9]*\.([a-zA-Z]{2,3})((?:\.[a-zA-Z]{2}))?" # TODO still needs debugging
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"
    
    # check validity of input destination
    if destination is not None:
        # verify if IP address was entered that it was entered properly
        if re.match(ip_pattern, destination):
             return True, destination
        # if an IP address was not entered, retrieve IP address based on URL
        else:
            try:
                socket.gethostbyname(destination)
            # an error has occured within socket
            except socket.gaierror:
                    return False, "Invalid URL. Try again."
            # accounting for urls with special characters/structures (i.e. https://, .en, etc.)
            else:
                dest_split = parse.urlsplit(destination)
                dest_ip = socket.gethostbyname(dest_split.netloc)

                destination = dest_ip
                return True, destination
    # no entry made
    else:
        return False, "Must enter a URL to begin."

if __name__ == "__main__":
    result, message = dest_address("tate.org.uk")
    print(message)