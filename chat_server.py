
## number of chatrooms
chatrooms = []

## all the join_ids
## ip_address of chat room , port of chat room
## error code integer
## 

join_id = 0


## sending initial message to client before sending other messages
def newclient(conn):
	data = conn.recv(4096)
	## extract the chatroom name
	## should there be different ip_addresses and diferent port numbers for different chat rooms
	## try sending the message 
	message = 'JOINED_CHATROOM : ', '\n', 'SERVER_IP: 0.0.0.0', '\n', 'PORT: 8888', '\n', 'ROOM_REF:', ROOM_REF, '\n', 'JOIN_ID:]', join_id
	conn.send(message)
	in specific chatroom
		connection_list1.append(conn)
		msg = 'client name has joined the chatroom'
		broadcastmessage(chatroom, msg)

def client_leaving(conn, data):
	print " LEFT_CHATROOM: [ROOM_REF]", '\n', 'JOIN_ID: [integer previously provided by server on join]', '\n'
	## post a message to relevant chatroom indicating that client has disconnected
## dont terminate the connection

def terminationg connection ():

def newdata(conn, data):
	## make cases of simple msg, leaving, terminating  ## create the corresponding functions of these 
	msg = ' LEFT_CHATROOM:', ROOM_REF, '\n', 'JOIN_ID:',join_id, '\n'
	conn.send(msg)
	to relevant chatroom:
	msg = 'client name has disconnected'
	broadcastmessage(msg)
	connection_listn.remove(conn)





## starting with the server
if __name__ == "__main__":
	## number of connections
	connection_list = []
	## create a server socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	## server port  ## server ip address - '0.0.0.0'
	port = 8888
	s.bind(('0.0.0.0', port))
	## no of listening connections
	s.listen(10)
	while 1:
		#try:
		ready_to_read, ready_to_write, error_sockets = select.select(connection_list, [], [])
		for sock in ready_to_read:
			if sock == s:
				conn, addr = s.accept()
				start_new_thread(newclient, (conn,))
				#connection_list.append(conn)
			else:    ## may use the function client disconnected
				data = conn.recv(4096)
				start_new_thread(newdata, (conn, data))
				## either it is the message or client leaves or terminate connection
		except:
			#def error in msg   ...









'''## using threads we have a separate handling code to handle all connections 
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
'''
