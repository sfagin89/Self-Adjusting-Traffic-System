import socket

# Creating Socket Object
s = socket.socket()
print ("Socket successfully created")

# Reserving Port
port = 3600

# Binding to port
s.bind(('', port))
print ("socket bound to %s" %(port))

# put the socket into listening mode
s.listen(5)
print ("socket is listening")

# Loop until error or interrupt
while True:

# Establish connection with client.
  c, addr = s.accept()
  print ('Got connection from', addr )

  # Test, respond to connection.
  c.send('Thank you for connecting'.encode())

  #rcvmsg = c.recv(1024)
  # Print to the console
  #print(rcvmsg.decode());

  # Write to a file
  rcvfile = c.recv(1024)
  f = open('rcvd_file.txt','wb')
  while rcvfile:
      f.write(rcvfile)
      rcvfile = c.recv(1024)
  f.close

  # Close the connection with the client
  c.close()

  # Breaking once connection closed
  break
