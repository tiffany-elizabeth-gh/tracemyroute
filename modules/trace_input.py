import re


def validate_trace_ip(destination):

    # variables needed to begin a trace
    destination = ""
    #source_addr = default
    max_hops = 50   # OPTIONAL ADD ON user input for max_hops
    #timeout = 2    # OPTIONAL timeout if necessary
    
    
    
    # user initiates trace by entering a destination
    # the destination is either a URL/website or IP address
    destination = input("Enter a destination (URL/IP): ")

    # define qualifications for destination input
    url_pattern = r"((https?\:\/\/)?((?:www\.))?)[a-zA-Z]+[0-9]*\.([a-zA-Z]{2,3})((?:\.[a-zA-Z]{2}))?"
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"
    
    # check validitiy of input destination
    if destination != "":
        if re.match(url_pattern, destination):
            return True, "Valid URL"
        elif re.match(ip_pattern, destination):
            return True, "Valid IP"
        else:
            return False, "Invalid input. Please enter a valid URL or IP address."
    else:
        return False, "Invalid input. Please enter a valid URL or IP address."
    

while True:
    destination = input("Enter a destination (URL/IP): ")
    result, err_str = validate_trace_ip(destination)

    if result == False:
        print(err_str, "try again!")
    else:
        break



if __name__ == "__main__":
    validate_trace_ip("")

# Will eventually bring source_address() in trace_input() 
# because it makes more sense for them to be in the same code



    
