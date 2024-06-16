# building the main code all together

from validate_trace_ip import trace_import

destination = input("Enter a destination (URL/IP): ")
valid_dest = validate_trace_ip(destination)
