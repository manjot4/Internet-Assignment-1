## client api
import requests, json, os
import os.path
from pathlib import Path
## client says to client proxt that it wants to read this file
# will do version check later on
filename = 'first.txt'	

def gng_to_dir_ser(filename):
	print 'starting the process to go to file_server\n'
	response = requests.get('http://0.0.0.0:8080/'+str(filename))
	print 'gng to dir server'
	response = response.text
	response = json.loads(response)
	filedir = response[str(filename)]
	port = response['port']
	print 'filedir: ', filedir
	print 'port:', port
	return str(filedir), str(port)

def gng_to_file_ser(filedir, port, filename):
	response = requests.get('http://0.0.0.0:'+str(port)+'/'+str(filename), json = {'file_info': str(filedir)})  
	response = response.text
	response = json.loads(response)
	file_data = response['file_data']
	return file_data
	

def readfile(filename):
	# check if file exists locally
	newpath = '/Users/manjotsingh/desktop/local_files' 
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	file_path = '/Users/manjotsingh/desktop/local_files/'+str(filename)
	filepath = Path(str(file_path))
	if filepath.is_file():   # checking if file is there -> got to dir server -> file server, version, then read file locally
		f = open(str(file_path), 'r')
		data = f.read()
		f.close()
		print 'file_data got locally'
		print data	  # will be returning this data over back to client
	else:
		filedir, port = gng_to_dir_ser(filename)
		file_data = gng_to_file_ser(filedir, port, filename) 
		print 'printing file_data\n', file_data  
		# caching it
		f = open(str(file_path), 'w') # writing data in a file
		f.write(file_data)
		f.close() 

def writefile(filename, content):
	# will do caching for this soon
	# first got to lock server
	response = requests.get('http://0.0.0.0:8082/'+str(filename))
	print 'gone to lock server'
	response = response.text
	print 'response', response
	response = json.loads(response)
	print 'checking'
	status = response['status']  

## checking to go for file server..
	if str(status) == 'sent':
		# gng to dir server to get data
		filedir, port = gng_to_dir_ser(filename)
		## going to file_Server
		response = requests.post('http://0.0.0.0:'+str(port)+'/'+str(filename), json = {'file_info': str(filedir) , 'summary': str(content)})
		response = response.text
		response = json.loads(response)
		status = response['writing']
		print 'status:', status
		# when writing is done, go to ls, to release key..
		posting = requests.post('http://0.0.0.0:8082/'+str(filename))
		posting = json.loads(posting.text)
		status = posting['status']
		print 'status', status
	else:
		print 'come back later'  ## write abort function..



'''
#before running, it makes a local folder on client side
newpath = '/Users/manjotsingh/desktop/local_files' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

# can give newpath to it
file_path = '/Users/manjotsingh/desktop/local_files/'+str(filename)
filepath = Path(str(file_path))
if filepath.is_file():   # checking if file is there -> got to dir server -> file server, version, then read file locally
	f = open(str(file_path), 'r')
	data = f.read()
	f.close()
	print 'file_data got locally'
	print data	  # will be returning this data over back to client
else:
	print "starting the process to get the file from server"
	response = requests.get('http://0.0.0.0:8080/'+str(filename))
	print 'got file name '
	response = response.text
	response = json.loads(response)
	#filepath = response[filename]
	filedir = response[str(filename)]
	port = response['port']
	#print 'filepath:', filepath
	print 'filedir: ', filedir
	print 'port:', port  

	## gng to server  // now change server...
	response = requests.get('http://0.0.0.0:'+str(port)+'/'+str(filename), json = {'file_info': str(filedir)})  
	response = response.text
	response = json.loads(response)
	file_data = response['file_data']
	print 'printing file_data\n', file_data  # returning this data back to client...

# for caching
	f = open(str(file_path), 'w')
	f.write(file_data)
	f.close() 



## client going to ls and gets data

response = requests.get('http://0.0.0.0:8082/'+str(filename))
print 'gone to lock server'
response = response.text
response = json.loads(response)
print 'checking'
#lock_key = response['key']
status = response['status']  ## should be sent for going to dir server, else rejected...for now

## checking to go for file server..
if str(status) == 'sent':
	## going to file_Server
	response = requests.post('http://0.0.0.0:'+str(port)+'/'+str(filename), json = {'file_info': str(filedir) , 'summary': 'writing experimentation again and again'}) # appending
	response = response.text
	response = json.loads(response)
	status = response['writing']
	print 'status:', status
else:
	pass  ## either loop again or abort
'''





