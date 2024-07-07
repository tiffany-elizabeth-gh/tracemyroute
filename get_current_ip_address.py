import socket
import requests

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"Your Computer IP Address is: {local_ip}")

