## CHAT SERVER 
## MANJOT SINGH
## 16338467

## importing all libraries
import re, sys
from thread import *
import socket, select

## separates numbers and text
r = re.compile("(\s)([a-zA-Z]+)([0-9]+)")

## list of chatrooms
chatrooms = []   ## contains number of chatrooms

## contains relevant clients in every chatrooms
client_list = [[],[],[]]

## it contains reqd connections in every chatrooms 
lists = [[],[],[],[],[],[],[],[],[]]  



## function to send joining message to chatroom
def broadcast_data(ROOM_REF, conn, message):		
	for socke in lists[int(ROOM_REF)]:   ## considering every socket in that chatroom
		if socke != s:
			socke.send(message)   	

## sending client the join message
def send_join_message(conn, room_name, ROOM_REF, client_name, client_no):
	## send the message to client 
	message = 'JOINED_CHATROOM:'+ str(room_name)+'\nSERVER_IP:10.62.0.47\nPORT:8888\nROOM_REF:'+ str(ROOM_REF)+'\nJOIN_ID:'+ str(client_no)+'\n'
	conn.send(message)
## now send the message to that chatroom
	if int(ROOM_REF) in chatrooms:
		msg = 'CHAT:'+str(ROOM_REF)+'\nCLIENT_NAME:'+str(client_name)+'\n'+'MESSAGE:'+str(client_name) + ' has joined this chatroom.\n\n'
		lists[int(ROOM_REF)].append(conn)
		broadcast_data(ROOM_REF, conn, msg)

## joining the chatroom
def join_chatroom(conn, data):
	extract = [] ## relevant data will be stored here...
	## extract relevant data like client name, chatroom name etc. 
	ext = data.split('\n')
	for i in ext:
		b = i.split(':')
		extract.append(b)
	room_name = extract[0][1]
	## extract the client_name
	client_name = extract[3][1]  
	## getting the room ref number from chatroom name
	m = r.match(extract[0][1])
	ROOM_REF = m.group(3)
	## join_id will be client no
	a = r.match(extract[3][1])
	client_no = a.group(3)
	## appending client no in client_list
	client_list[int(ROOM_REF)].append(client_no)   
	## appending room_ref in chatrooms
	if ROOM_REF not in chatrooms:
		chatrooms.append(int(ROOM_REF))  	
	## sending message to client for joining
	send_join_message(conn, room_name, ROOM_REF, client_name, client_no)


## function to send leaving messages to chatroom
def broadcast_data_leaving(ROOM_REF, conn, message):		
	for socke in lists[int(ROOM_REF)]:
		if socke != s:
			socke.send(message)
	lists[int(ROOM_REF)].remove(conn)

## sending leave message to client
def send_leave_message(conn, ROOM_REF, join_id, client_name):
	## send the message to client
	message = 'LEFT_CHATROOM:'+str(ROOM_REF)+'\nJOIN_ID:'+str(join_id)+'\n'
	print 'sending message left'
	conn.send(message)
	## posting a message in relevant chatroom
	if int(ROOM_REF) in chatrooms:
		msg = 'CHAT:'+str(ROOM_REF)+'\nCLIENT_NAME:'+str(client_name)+'\n'+'MESSAGE:'+str(client_name) + ' has left this chatroom.\n\n'
		broadcast_data_leaving(ROOM_REF, conn, msg)

## leaving chatroom
def leave_chatroom(conn, data):
	extract = []
	## extract the room reference number, join_id and client_name
	ext = data.split("\n")
	for i in ext:
		b = i.split(':')
		extract.append(b)
	ROOM_REF = extract[0][1]  ## IN STRINGS
	join_id = extract[1][1]
	client_name = extract[2][1]
	# join_id will be client_no 
	a = r.match(extract[2][1])
	client_no = a.group(3)
	client_list[int(ROOM_REF)].remove(client_no)
	## calling send leave message function
	send_leave_message(conn, ROOM_REF, join_id, client_name)

## sending chat message in every chatroom
def sending_message(conn, ROOM_REF, client_name, message):
	## sending the message
	data = 'CHAT:'+str(ROOM_REF)+'\nCLIENT_NAME:'+str(client_name)+'\nMESSAGE:'+str(message)+'\n\n'
	if int(ROOM_REF) in chatrooms: 
		broadcast_data(ROOM_REF, conn, data)

## messaging chatroom
def msg_chatroom(conn, data):
	extract = []
	## extract the room reference number, join_id, client_name and message
	ext = data.split('\n')
	for i in ext:
		b = i.split(':')
		extract.append(b)
	ROOM_REF = extract[0][1]
	join_id = extract[1][1]
	client_name = extract[2][1]
	message = extract[3][1]
	## sending message to everyone in that chatroom
	sending_message(conn,ROOM_REF, client_name, message)

## sending data about client disconnecting in every chatroom
def broadcast_data_disconnect(ROOM_REF, conn, message, client_no):		
	for socke in lists[(ROOM_REF)]:
		if socke != s:
			socke.send(message)
	lists[(ROOM_REF)].remove(conn)  ## removing the client connection from every chatroom

## disconnecting service
def disconnecting_service(conn, data):
	extract = []
	## extracting client_name, client_no 
	ext = data.split('\n')
	for i in ext:
		b = i.split(':')
		extract.append(b)
	client_name = extract[2][1]
	a = r.match(extract[2][1])
	client_no = a.group(3)
	## if a particular connection is to be terminated, it should be removed from every connection list
	## terminating the connection
	connection_list.remove(conn)
	for i in range(1,3):
		if client_no in client_list[i]:
			msg = 'CHAT:'+str(i)+'\nCLIENT_NAME:'+str(client_name)+'\n'+'MESSAGE:'+str(client_name) + ' has left this chatroom.\n\n'
			client_list[i].remove(client_no)
			broadcast_data_disconnect(i, conn, msg, client_no)



def newdata(conn, data):
	## splitting the data
	info = data.split(':')
	print info[0]
	if (info[0] == 'JOIN_CHATROOM'):
		# make a function for join chatroom
		join_chatroom(conn, data)
	elif (info[0] == 'LEAVE_CHATROOM'):
		# make a function for leave chatroom
		leave_chatroom(conn, data)
	elif (info[0] == 'CHAT'):
		# make a function for message chatting
		msg_chatroom(conn, data)
	elif (info[0] == 'DISCONNECT'):
		## make a function for disconnecting service
		disconnecting_service(conn, data)
	elif (info[0] == 'HELO BASE_TEST\n'):
		msgg = 	'HELO BASE_TEST\nIP:10.62.0.47\nPORT:8888\nStudentId:16338467\n'
		conn.sendall(msgg)	
 


## starting with the server
if __name__ == "__main__":
	## total number of connections
	connection_list = []
	## create a server socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	## server port  
	port = 8888
	s.bind(('0.0.0.0', port))
	## no of listening connections; by default takes 5 at a time.
	s.listen(10)  
	connection_list.append(s)
	while 1:
		## reading the server socket
		ready_to_read, ready_to_write, error_sockets = select.select(connection_list, [], [])
		for sock in ready_to_read:
			if sock == s:   ## main socket has some data
				conn, addr = s.accept()   ## accepting new connections
				connection_list.append(conn)
			else:  ## getting new connections
				data = sock.recv(4096)  
				if (data == 'KILL_SERVICE\n'):     
					sys.exit()  ## stop the server if KILL_SERVICE msg received
				else:
					start_new_thread(newdata, (sock, data))  ## start new thread for every connection







