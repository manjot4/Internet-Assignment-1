## open a socket
## bind to address and port
## listen to incoming connections
## accept connections
## read/send
##  server handles multiple chat clients with select baesd multiplexing.
## chat client must be connected to same port
## if any client sockets is readable, then client has send message to server

## using threads we have a separate handling code to handle all connections 
import socket, select
import sys
from thread import *

## function to broadcast chat messages to all connected clients
def broadcast_data(sock, message):
	for socke in connection_list:
		if socke != s and socke != sock:
			try:
				socke.send(message)
			except:
				socke.close()
				connection_list.remove(socke)	

if __name__ == "__main__":
	## list to keep track of clients and socket descriptors
	connection_list = []
	
	port = 5000

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## dont know what this line is for
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('0.0.0.0', port))
	## try if not specifying number, can we listen to any number of clients ?
	s.listen(10)

	connection_list.append(s)
	print "chat server started on port ", str(port)
	while 1:
		## we create new sockets for incoming connections
		## get the list of new sockets which are ready to be read trhough select
		ready_to_read, ready_to_write, error_sockets = select.select(connection_list, [], [])

		for sock in ready_to_read:
			## if master socket is readable , it means a new connection
			if sock == s:
				sock_new, addr = s.accept()
				## sock_new is a new socket
				connection_list.append(sock_new)
				print "Client (%s, %s) connected" % addr

				## broadcasting the data that client has entered the room
				broadcast_data(sock_new, "[%s:%s] entered room\n" % addr)

		## else there is some incoming message from a client
			else:
				try:
					## process data received from client
					data = sock.recv(4096)
					if data:
						broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
				except:
					broadcast_data(sock, "Client (%s, %s) is offline" % addr)
					print "Client (%s, %s) is offline" % addr
					sock.close()
					connection_list.remove(sock)
					continue
	s.close()






'''host = ''
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

## binding the socket
try:
    s.bind((host, port))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

## you cannot bind two sockets to the same port
## 10 is the number of incoming connections that are kept waiting if the program is busy


s.listen(10)
print 'socket now listening'

## function for handling conncetions. This will be used to create threads

## while 1:  put in a loop, live srever,, conn.sendall() comes in this

conn, addr = s.accept()
#display client information
print 'Connected with ' + addr[0] + ':' + str(addr[1])

data = conn.recv(1024)

conn.sendall(data)
 
conn.close()
s.close()'''

'''def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data: 
            break
     
        conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()'''
