# DELETE - unnecessary module

import re


def validate_trace_ip(destination):

    # define qualifications for destination input
    url_pattern = r"((https?\:\/\/)?((?:www\.))?)[a-zA-Z]+[0-9]*\.([a-zA-Z]{2,3})((?:\.[a-zA-Z]{2}))?"
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"
    
    # check validity of input destination
    if destination != None:
        if re.match(url_pattern, destination):
            return True, "Valid URL"
        elif re.match(ip_pattern, destination):
            return True, "Valid IP"
        else:
            return False, "Invalid input. Please enter a valid URL or IP address."
    else:
        return False, "Invalid input. Please enter a valid URL or IP address."
    


if __name__ == "__main__":

    while True:
        destination = input("Enter a destination (URL/IP): ")
        result, err_str = validate_trace_ip(destination)

        if result == False:
            print(err_str, "try again!")
        else:
            break
   

# Will eventually bring source_address() in trace_input() 
# because it makes more sense for them to be in the same code



    
