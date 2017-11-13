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
	a = 5	
	#connection_list = [s, sys.stdin]
	#connection_list.append(s)
	print 'Connected to remote host. Start sending messages'
	#msg = 'JOIN_CHATROOM: room1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client1'
	#s.sendall(msg)
	while True:
		connection_list = [s, sys.stdin]
		ready_to_read, ready_to_write, error_sockets = select.select(connection_list, [], [])
		for sock in ready_to_read:
			if sock == s:
				data = sock.recv(1024)
				print data
			else:
				msg = sys.stdin.read()
				s.send(msg)	
	#msg = 'JOIN_CHATROOM: room2\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client1'
	#s.sendall(msg)
	#data = s.recv(1024)
	#print data
	#a = 6