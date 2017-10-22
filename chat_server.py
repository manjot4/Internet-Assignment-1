

## making a connection doesn't mean that data is being sent
## recv data, make a function to identify data, either it could be:
## 1. join a chatroom -- make a join_chatroom function ----done
## --> make a function which sends message to client  ---done 
## --> make a function which broadcasts the message --- done
## 2. leave a chatroom
## --> recv data and identify data.. make a fnc to send a msg leave msg -- done
## --> post a msg to relevant chatroom, --done
## 3. send a message to a chatroom
## --> recv the message, parse it and make a fnc to broadcast message -- done
## 4. Disconnect service 
## -> terminate the client-server connection.. -- done

	
	## should there be different ip_addresses and diferent port numbers for different chat rooms
## create different connection lists

# splitting 1 from room1
import re
r = re.compile("([a-zA-Z]+)([0-9]+)")



## list of chatrooms
chatrooms = []

## all the join_ids
join_ids = []
join_id = 1


## function to broadcast chat messages to all connected clients
def broadcast_data(ROOM_REF, conn, message):
	for socke in connection_list[ROOM_REF]:   #### ---- ?????
		if socke != s and socke != conn:
			socke.send(message)  ## broadcast msg to every client in that chatroom 	

def send_join_message(conn, room_name, ROOM_REF, client_name):
	## send the message to client 
	message = 'JOINED_CHATROOM :', room_name, '\n', 'SERVER_IP: 0.0.0.0', '\n', 'PORT: 8888', '\n', 'ROOM_REF:', ROOM_REF, '\n', 'JOIN_ID:]', join_id
	conn.send(message)
	## appending join_id
	join_ids.append(join_id)
	## incrementing join_id
	join_id = join_id + 1
	## now send the message to that chatroom
	for i in chatrooms:
		if i == ROOM_REF:
			lists.append()      ### ---- ?????
			msg = client_name, 'has joined the chatroom'
			broadcast_data(ROOM_REF, conn, msg)

def join_chatroom(conn, data):
	## extract the chatroom name
	extract = data.split(":")
	room_name = extract[0]
	## extract the client_name
	client_name = extract[3]  ## not final
	## getting the room ref number from chatroom name
	m = r.match(room_name)
	ROOM_REF = m.group(2)
	## appending room_ref in chatrooms
	chatrooms.append(ROOM_REF)
	send_join_message(conn, room_name, ROOM_REF, client_name)

def send_leave_message(conn, ROOM_REF, join_id, client_name):
	## send the message to client
	message = 'LEFT_CHATROOM:', ROOM_REF, '\n', 'JOIN_ID:', join_id
	conn.send(message)
	## posting a message in relevant chatroom
	for i in chatrooms:
		if i == ROOM_REF:
			lists.remove(conn) #--->????? 
			msg = client_name, 'has left the chatroom'
			broadcast_data(ROOM_REF, conn, msg)

def leave_chatroom(conn, data):
	## extract the room reference number, join_id and client_name
	extract = data.split(":")
	ROOM_REF = extract[1]
	join_id = extract[3]
	client_name = extract[5]
	## calling send leave message function
	send_leave_message(conn, ROOM_REF, join_id, client_name, message)

def sending_message(conn, ROOM_REF, client_name, message):
	## sending the message
	data = 'CHAT:', ROOM_REF, '\n', 'CLIENT_NAME:', client_name, '\n', 'MESSAGE:', message, '\n', '\n'
	for i in chatrooms:
		if i == ROOM_REF:
			broadcast_data(ROOM_REF, conn, data)

def msg_chatroom(conn, data):
	## extract the room reference number, join_id, client_name and message
	extract = data.split(":")
	ROOM_REF = extract[1]
	join_id = extract[3]
	client_name = extract[5]

	message = extract[7]
	## sending message to everyone in that chatroom
	sending_message(conn,ROOM_REF, client_name, message)

def disconnecting_service(conn, data):
	# extracting the client_name
	client_name = extract[5]
	### if a particular connection is to be terminated, it should be removed from every connection list
	## terminating the connection
	connection_list.remove(conn)

def newdata(conn, data):
	info = data.split(':')
	if info[0] == 'JOIN_CHATROOM':
		# make a function for join chatroom
		join_chatroom(conn, data)
	elif info[0] == 'LEAVE_CHATROOM'
		# make a function for leave chatroom
		leave_chatroom(conn, data)
	elif info[0] == 'CHAT':
		# make a function for message
		msg_chatroom(conn, data)
	else:
		## make a function for disconnecting service
		disconnecting_service(conn, data)	 



## starting with the server
if __name__ == "__main__":
	## total number of connections
	connection_list = []
	## create a server socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	## server port  ## server ip address - '0.0.0.0'
	port = 8888
	s.bind(('0.0.0.0', port))
	## no of listening connections
	s.listen()
	connection_list.append(s)
	while 1:
		ready_to_read, ready_to_write, error_sockets = select.select(connection_list, [], [])
		for sock in ready_to_read:
			if sock == s:
				conn, addr = s.accept()
				#start_new_thread(newclient, (conn,))  #----
				connection_list.append(conn)
			else: 
				try:
					## may use the function client disconnected
					data = sock.recv(4096)
					start_new_thread(newdata, (sock, data))  
				except:
					data = 'ERROR CODE :', integer  ## dont know this integer
					sock.send(data)









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
