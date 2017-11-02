

import re
r = re.compile("(\s)([a-zA-Z]+)([0-9]+)")

##error message numbers
integer = 0
## list of chatrooms
chatrooms = []
from thread import *
import socket, select

client_list = []
## make connection list for each room
lists = [[],[],[],[],[],[],[],[],[]]  ## considering 4 chatrooms......0,1,2,3

## function to broadcast chat messages to all connected clients
def broadcast_data(ROOM_REF, conn, message):
	for socke in lists[int(ROOM_REF)]:
		if socke != s:
			socke.send(message)   ## broadcast msg to every client in that chatroom 	

def send_join_message(conn, room_name, ROOM_REF, client_name, client_no):
	## send the message to client 
	message = 'JOINED_CHATROOM :'+ str(room_name)+'\nSERVER_IP: 0.0.0.0\nPORT: 8888\nROOM_REF:'+ str(ROOM_REF)+'\nJOIN_ID:'+ str(client_no)
	conn.send(message)
## now send the message to that chatroom
	if int(ROOM_REF) in chatrooms:
		msg = str(client_name) + ' has joined this chatroom'
		lists[int(ROOM_REF)].append(conn)
		broadcast_data(ROOM_REF, conn, msg)

def join_chatroom(conn, data):
	extract = []
	## extract the chatroom name
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
	a = r.match(extract[3][1])## giving join_id corresponding to client no..
	client_no = a.group(3)
	## appending room_ref in chatrooms
	if ROOM_REF not in chatrooms:
		chatrooms.append(int(ROOM_REF))  ## creating a room
		#lists.append([])  ## check out for insert
	## making a separate connection list for chatroom	

	send_join_message(conn, room_name, ROOM_REF, client_name, client_no)


def send_leave_message(conn, ROOM_REF, join_id, client_name):
	## send the message to client
	message = 'LEFT_CHATROOM:'+str(ROOM_REF)+'\nJOIN_ID:'+str(join_id)
	conn.send(message)
	## posting a message in relevant chatroom
	if int(ROOM_REF) in chatrooms:
		lists[int(ROOM_REF)].remove(conn)
		msg = str(client_name)+'has left the chatroom'
		broadcast_data(ROOM_REF, conn, msg)

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
	## calling send leave message function
	send_leave_message(conn, ROOM_REF, join_id, client_name)

def sending_message(conn, ROOM_REF, client_name, message):
	## sending the message
	data = 'CHAT:'+str(ROOM_REF)+'\nCLIENT_NAME:'+str(client_name)+'\nMESSAGE:'+str(message)+'\n\n'
	if int(ROOM_REF) in chatrooms: 
		broadcast_data(ROOM_REF, conn, data)

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


def newdata(conn, data):
	print 'hello'
	info = data.split(':')
	if info[0] == 'JOIN_CHATROOM':
		# make a function for join chatroom
		join_chatroom(conn, data)
	elif info[0] == 'LEAVE_CHATROOM':
		# make a function for leave chatroom
		leave_chatroom(conn, data)
	elif info[0] == 'CHAT':
		# make a function for message chatting
		msg_chatroom(conn, data)
	elif info[0] == 'DISCONNECT':
		## make a function for disconnecting service
		disconnecting_service(conn, data)	 


def disconnecting_service(conn, data):
	extract = []
	## extracting client_name 
	ext = data.split('\n')
	for i in ext:
		b = i.split(':')
		extract.append(b)
	client_name = extract[2][1]
	### if a particular connection is to be terminated, it should be removed from every connection list
	## terminating the connection
	connection_list.remove(conn)

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
	s.listen(10)
	connection_list.append(s)
	while 1:
		ready_to_read, ready_to_write, error_sockets = select.select(connection_list, [], [])
		for sock in ready_to_read:
			if sock == s:
				conn, addr = s.accept()
				print 'connection connecting'
				#start_new_thread(newclient, (conn,))  #----  while making new connection, how does I know it sends message in it
				connection_list.append(conn)
			else: 
				#try:

				data = sock.recv(4096)
				start_new_thread(newdata, (sock, data))  
				#except:
				#	global integer
				#	integer = integer + 1
				#	data = 'ERROR CODE:'+ integer+'\nERROR_DESCRIPTION: Not able to connect.'  ## dont know this integer
				#	sock.send(data)






