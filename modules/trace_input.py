import re



def trace_input():

    # variables needed to begin a trace
    
    destination = ""
    source_addr = default
    max_hops = 50   # OPTIONAL ADD ON user input for max_hops
    #timeout = 2    # OPTIONAL timeout if necessary
    
    
    
    # user initiates trace by entering a destination
    # the destination is either a URL/website or IP address
    destination = input("Enter a destination (URL/IP): ")

    # define qualifications for destination input
    url_pattern = r"((https?:\/\/[\w+-_]+.)|([\w+-_]+.)){1}([\wñÑ+-_]+.{1}[\w+]{2,10})"
    ip_pattern = r"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)"
    
    # check validitiy of input destination
    if destination is "":
        if re.match(url_pattern, destination):
            print("Valid URL")
        elif re.match(ip_pattern, destination):
            print("Valid IP")
    else:
        print("Invalid input. Please enter a valid URL or IP address.")






    # OPTIONAL
    # add the optional user input for a starting IP address 
    # this would allow the user to specify a specific starting point for the trace
