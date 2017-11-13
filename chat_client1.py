## importing libraries
import socket, select, string
import sys  

def prompt():
	sys.stdout.write('You : ')
	sys.stdout.flush()

if __name__ == "__main__":
#	if(len(sys.argv) < 3) :
#		print 'Usage : python telnet.py hostname port'
#		sys.exit()

	host = 'localhost'
	port = 8888

	## creating the socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.settimeout(2)
	## connect to remote host
	try:
		s.connect((host, port))
	except:
		print "unable to connect"
		sys.exit()
	print 'Connected to remote host. Start sending messages'
	msg = 'JOIN_CHATROOM: room2\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client2'
	s.send(msg)
	while True:
		data = s.recv(4096)
		print data
	#msg = 'JOIN_CHATROOM: room2\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client1'
	#s.send(msg)
	#data = s.recv(4096)
	#print data