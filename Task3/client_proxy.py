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

## client gets all info about file server...
## sending filepath which is received from dir server along with filename
response = requests.get('http://0.0.0.0:'+str(port)+'/'+str(filename), json = {'file': str(filepath)})  
response = response.text
response = json.loads(response)
file_data = response['file_data']
print 'printing file_data\n', file_data
