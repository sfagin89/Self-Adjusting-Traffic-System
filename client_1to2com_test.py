import socket

# Creating Socket
# AF_INET = IPv4
# SOCK_STREAM = TCP protocol
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

# Port set for Node Communication Socket
port = 3600

try:
    host_ip = socket.gethostbyname('192.168.0.20')
except socket.gaierror:

    # this means could not resolve the host
    print ("there was an error resolving the host")
    sys.exit()

# connecting to the server
s.connect((host_ip, port))

print ("The socket has successfully connected to node02")
