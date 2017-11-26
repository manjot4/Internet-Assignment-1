## client api
import requests, json

## client says to client proxt that it wants to read this file

filename = 'first.txt'
# client gives the name of the file
## client api will got to dierc

response = requests.get('http://0.0.0.0:8080/'+str(filename))
print 'got file name '
response = response.text
response = json.loads(response)
filepath = response[filename]
port = response['port']
print 'filepath:', filepath
print 'port:', port

## if read perform below things::

## client gets all info about file server...
## sending filepath which is received from dir server along with filename

#response = requests.get('http://0.0.0.0:'+str(port)+'/'+str(filename), json = {'file': str(filepath)})  
#response = response.text
#response = json.loads(response)
#file_data = response['file_data']
#print 'printing file_data\n', file_data


# if write -- perform below things :::
## for modifying the file, client first goes to ls, gets the key, then goes to ds, then to fs....

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
	response = requests.post('http://0.0.0.0:'+str(port)+'/'+str(filename), json = {'file': str(filepath) , 'summary': 'writing experimentation again and again'}) 
	response = response.text
	response = json.loads(response)
	status = response['writing']
	print 'status:', status
else:
	pass  ## either loop again or abort






