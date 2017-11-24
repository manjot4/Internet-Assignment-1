from flask import Flask, jsonify, request
import requests
fs.run = Flask(__name__)

## file server is going to be called by client api
##--> client will either ask for file access
## -> server must give client the file...
## when writing stuff, 1. check the version of file that client wrote.. if new update the file 
## later work -- client needs to make sure that it has correct version of file at what time ???..

## file server is going to be called by directory server -- for what...
## 

file_direc = [
	{'id' : 'mantena.rtf',
	'filename' : '/Users/manjotsingh/desktop/mantena.rtf',
	'version': 0 }
	{'id' : 'second.rtf',
	'filename' : '/Users/manjotsingh/desktop/second	.rtf',
	'version': 0 }


## return file to client
@fs.route('/',methods=['GET'])    
def get_file():                      ## all for getting new file to read 
    file_name = request.args.get('file')   ## check it with strings
    for files in file_direc:
    	if files['id'] == file_name :
    		info = {'machine id': '', 'path to file' : files['filename']}
    return jsonify(info)


@fs.route('/', methods=['PUT'])
def update_file():
	file_name = request.args.get('file')
	file_version = request.args.get('version')
	for files in file_direc:
		if files['id'] == file_name:
			if files['version'] < file_version:
				update_info = ## get either the file or filename
				return jsonify(update_info)




## fs asks for machine id from dir server
def machine_id():
	machine_id = requests.get('end point', )
	## get machine id by any way


## once it gets machine id, it give direc server a list of files it has with it.
	info = requests.post('end point ', data = all info for files)

if __name__ == '__main__':
	fs.run(debug=True, port = 8081, host = '0.0.0.0')
	## as soon as it wakes up, registers with directory server for machine id

