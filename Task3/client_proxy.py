# Name - Manjot Singh
# Student Id - 16338467
# Program Name - client_proxy.py
# ------------------------------------------------------#
# libraries stuff
import requests, json, os
import os.path
from pathlib import Path
#-------------------------#

# this directory maintains all info of all files that a client has.
cache_direc = {}   # {client1: {file1 : version, file2 : version}, client2 : {file1:version, file2:version} }

# going to directory server and get all information
def gng_to_dir_ser(filename):
	# gets port number of file server and name of file directory from directory server
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

# going to file server to read files remotely
def gng_to_file_ser(filedir, port, filename):
	# gets file data and file version from file server
	response = requests.get('http://0.0.0.0:'+str(port)+'/'+str(filename), json = {'file_info': str(filedir)})  
	response = response.text
	response = json.loads(response)
	file_data = response['file_data']
	file_version = response['version']
	return file_data, file_version	

# going to file server to check the version of file it has and file saved. 
def gng_to_file(filedir, port, filename, version):
	# gets the status of whether version is same or not 
	response = requests.get('http://0.0.0.0:'+str(port)+'/', json = {'file_info': str(filedir), 'filename' : str(filename), 'version' : str(version)})  
	response = response.text
	response = json.loads(response)
	status = response['status']
	print status
	return status

# client itself send its client_id - might change this so that client proxy handles it
def initialize_dir(filename, client_id):
	filedirname = 'cache' + str(client_id)
	# create dir for that client if the directory doesn't exist/local directory where cached files are
	if not os.path.exists(str(filedirname)):
		os.makedirs(str(filedirname))
	return str(filedirname)

# client goes here asking to read files
def readfile(filename, client_id):
	global cache_direc
	# check if file exists locally
	#initialize the directory for that client
	filedirname = initialize_dir(filename, client_id)
	# filepath for file
	file_path  = str(filedirname) + '/' + str(filename) 
	# -----
	filepath = Path(str(file_path))
	if filepath.is_file():   # checking if file is there -> go to dir_server -> file server, check version, if same, then read file locally
		# going to dir server .... to get filedir and port
		filedir, port = gng_to_dir_ser(filename)
		# gng to file server.. to check the version of file .. first getting the version if file exists locally
		for i,v in cache_direc.items():
			if str(i) == str(client_id):
				for m,n in v.items():
					if str(m) == str(filename):
						ver = v[str(m)]
						print 'ver', ver

		# going to fileserver with filedir, port, version and filename				
		status = gng_to_file(filedir, port, filename, ver)
# if status is same , read file locally
		if (str(status) == 'same'):
			f = open(str(file_path), 'r')
			data = f.read()
			f.close()
			print 'file_data got locally'
			print data	  
		else:    
			# read file remotely 
			file_data, file_version = gng_to_file_ser(filedir, port, filename) 
			print 'printing file_data\n', file_data  
			print 'version', file_version
			f = open(str(file_path), 'w') # writing data in a file ... overwriting the file
			f.write(file_data)
			f.close() 
			# storing the new version
			for k,v in cache_direc.items():
				if str(k) == str(client_id):
					v.update({str(filename) : str(file_version)})
			
	else:
		# going to file server for first time to read the file
		print 'new file'
		filedir, port = gng_to_dir_ser(filename)
		file_data, file_version = gng_to_file_ser(filedir, port, filename) 
		print 'printing file_data\n', file_data  
		print 'version', file_version
# caching data/file
		f = open(str(file_path), 'w') # writing data in a file
		f.write(file_data)
		f.close() 
		info = {str(filename) : str(file_version)}
		cache_direc.update({str(client_id) : info})
		
		print cache_direc		

# client comes here if it has to write to a file
# writing is done remotely
def writefile(filename, client_id):
	# first go to lock server
	response = requests.get('http://0.0.0.0:8082/'+str(filename))
	print 'gone to lock server'
	response = response.text
	response = json.loads(response)
	print 'checking response'
	status = response['status']  
# if lock server says sent, then client canwrite
## checking to go for file server..
# everything that client writes, appends to a file
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
		# when writing is done, go to lock_server, to release key..
		posting = requests.post('http://0.0.0.0:8082/'+str(filename))
		posting = json.loads(posting.text)
		status = posting['status']
		print 'status', status
	else:
		print 'come back later'  ## polling

#######END OF CODE##############################		





