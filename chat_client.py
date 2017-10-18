## importing libraries
import socket, select, string
import sys  

def prompt():
	sys.stdout.write('You : ')
	sys.stdout.flush()

if __name__ == "__main__":
	if(len(sys.argv) < 3) :
		print 'Usage : python telnet.py hostname port'
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])

	## creating the socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	## connect to remote host
	try:
		s.connect((host, port))
	except:
		print "unable to connect"
		sys.exit()
	print 'Connected to remote host. Start sending messages'
	prompt()
	while 1:
		socket_list  = [sys.stdin, s]
## get the sockets that are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		for sock in read_sockets:
			if sock == s:
				## incoming message
				data = sock.recv(4096)
				if not data:
					print 'disconnected from chat server'
					sys.exit()
				else:
					print sys.stdout.write(data)
					prompt()
			else:
				## user entered a message
				msg = sys.stdin.readline()
				s.send(msg)
				prompt()



'''
try:
 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ## craeting a TCP socket
except socket.error, msg:
	print "failed to create socket. Error code" + str(msg[0]) + ',error message:' + msg[1]
	sys.exit() 	
print 'socket created'

host = 'www.google.com'
port = 80


## trying to get the ip_address
try:
	ip_address = socket.gethostbyname(host)
except socket.gaierror:
	print 'host name could not be resolved'
	sys.exit()
print "ip address of host is :" + ip_address 

## connect to remote server(arguments are passed as a tuple)
s.connect((ip_address, port))
print "socket connected to " + host + ' on address ' + ip_address	

#Send some data to remote server
message = "GET / HTTP/1.1\r\n\r\n"
try:
	s.sendall(message)
except socket.error:
	print 'send failed'
	sys.exit()	
print "message send successfully"

## receiving the reply from server
reply = s.recv(4096)
print reply
s.close
'''