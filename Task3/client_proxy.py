# multiple file servers - make 2 - to ensure that both registers with diff machine id
# ensure client goes to multiple file servers
# ------------------------------------------------------#
# will do tomorrow
# master raedy
# divide by total number
# check again cc with amber
# run on one more repository
#-------------------------#
# write script for chat server


## client api
import requests, json, os
import os.path
from pathlib import Path



cache_direc = {}   # {client1: {file1 : version, file2 : version}, client2 : {file1:version, file2:version} }

def gng_to_dir_ser(filename):
	print 'going to dir_server and starting the process to go to file_server\n'
	response = requests.get('http://0.0.0.0:8080/'+str(filename))
	print 'getting response from dir_server\n'
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
	file_version = response['version']
	return file_data, file_version	

# have to check which file dir server returns
def gng_to_file(filedir, port, filename, version):
	response = requests.get('http://0.0.0.0:'+str(port)+'/', json = {'file_info': str(filedir), 'filename' : str(filename), 'version' : str(version)})  
	response = response.text
	response = json.loads(response)
	status = response['status']
	print status
	return status


def initialize_dir(filename, client_id):
	filedirname = 'cache' + str(client_id)
	# create dir for that client
	if not os.path.exists(str(filedirname)):
		os.makedirs(str(filedirname))
	return str(filedirname)

def readfile(filename, client_id):
	global cache_direc
	# check if file exists locally
	#initialize the directory for that client
	#version = 0
	filedirname = initialize_dir(filename, client_id)
	# filepath for file
	file_path  = str(filedirname) + '/' + str(filename) 
	# -----
	filepath = Path(str(file_path))
	if filepath.is_file():   # checking if file is there -> got to dir server -> file server, version, then read file locally
		# going to dir server .... got filedir and port
		filedir, port = gng_to_dir_ser(filename)
		# gng to file server.. to check the version of file .. first getting the version if file exists locally
		for i,v in cache_direc.items():
			if str(i) == str(client_id):
				for m,n in v.items():
					if str(m) == str(filename):
						ver = v[str(m)]
						print 'ver', ver

		print  ver
		# going to fileserver with filedir, port, version and filename				
		status = gng_to_file(filedir, port, filename, ver)

		if (str(status) == 'same'):
			f = open(str(file_path), 'r')
			data = f.read()
			f.close()
			print 'file_data got locally'
			print data	  
		else:    # files server should also return version
			file_data, file_version = gng_to_file_ser(filedir, port, filename) 
			print 'printing file_data\n', file_data  
			print 'version', file_version
			f = open(str(file_path), 'w') # writing data in a file ... overwriting the file
			f.write(file_data)
			f.close() 
			for k,v in cache_direc.items():
				if str(k) == str(client_id):
					v.update({str(filename) : str(file_version)})
			
	else:
		print 'new file'
		filedir, port = gng_to_dir_ser(filename)
		file_data, file_version = gng_to_file_ser(filedir, port, filename) 
		print 'printing file_data\n', file_data  
		print 'version', file_version
		
		f = open(str(file_path), 'w') # writing data in a file
		f.write(file_data)
		f.close() 
		info = {str(filename) : str(file_version)}
		cache_direc.update({str(client_id) : info})
		
		print cache_direc		

def writefile(filename, client_id):
	# first go to lock server
	response = requests.get('http://0.0.0.0:8082/'+str(filename))
	print 'gone to lock server'
	response = response.text
	response = json.loads(response)
	print 'checking response'
	status = response['status']  

## checking to go for file server..
	if str(status) == 'sent':
		# ask the client to write
		content =  raw_input('Type to content to write\n')
		print 'content : \n', str(content)
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
		print 'come back later'  





