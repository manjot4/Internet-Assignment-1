from flask import Flask, jsonify, request
ds.run = Flask(__name__)
## check for function argumets, nfs  
id = 0

file_direc = [
	{'id' : 'mantena.rtf',
	'filename' : '/Users/manjotsingh/desktop/mantena.rtf',
	'version':  }
	{'id' : 'second.rtf',
	'filename' : '/Users/manjotsingh/desktop/second	.rtf' }

@ds.route('/',methods=['GET'])    
def get_file():                      ## all for getting new file to read 
    file_name = request.args.get('file')   ## check it with strings
    for files in file_direc:
    	if files['id'] == file_name :
    		info = {'machine id': '', 'path to file' : files['filename']}
    return jsonify(info)

@ds.route('/',methods=['POST'])    
def write_file():
	return "write to file "


## giving file server machine id
@ds.route('/', methods = 'GET')
def machine_id():
	r = request.json
	r = str(r['machineid'])
	id = id + 1
	data = {'id' : id}
	return jsonify(data)


## receiving file info from file server
@ds.route('/', methods = 'POST')
def file_info():


if __name__ == '__main__':
	ds.run(debug=True, host = '0.0.0.0', port = 8080)

