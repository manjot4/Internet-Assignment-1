# Name - Manjot Singh
# Student_Id - 16338467
# Program - directory_server.py
#-----------------------#
# libraries stuff 
from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
ds = Api(app)
#------------------------#

machines = {}  #stores all mapping{machine number : {file_directory :[list of files]},host, port }, } 
#{'1': {'files': [u'first.txt', u'second.txt'], 'files1': [u'second1.txt', u'first.txt'], 'host': '0.0.0.0', 'port': '8081'}, 2:.... }

# gives this id to every file server
id = 0

host = 0
port = 0

## giving client the machine id
class fs_id(Resource):
	# client comes in with machine id, host, port
	# returns registration as success.
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('machine_id', location = 'json')
		parser.add_argument('port', location = 'json')
		parser.add_argument('host', location = 'json')
		args = parser.parse_args()
		global host
		global port
		host = args['host']
		port = args['port']
		global id
		id = id+1
		return {'Registered': 'success', 'machine_id' : id}
ds.add_resource(fs_id, '/')

## updating his list of files
class fs_post(Resource):
	# client comes with file info it has and machine id given to it by dir_Server
	def post(self, machine_id):
		# all mapping is done now..which will result in machines folder
		# mapping file_direc to list of files for every directory
		global machines
		response = request.json
		dictn = {}
		for file_dir in response:
			fileess = response[str(file_dir)]
			info = {str(file_dir) : fileess}
			dictn.update(info)
		global host
		global port	
		dictn.update({'host':str(host)})
		dictn.update({'port':str(port)})
		name = str(machine_id)
		final_info = {name: dictn}
		machines.update(final_info)
		print 'machines : ', machines
		return {'data files_ds' : 'received'}
ds.add_resource(fs_post, '/<int:machine_id>')		

# client comes in with filename and dir_server gives back file_direc and port number of file server where the file is
## receiving name of file and giving back port and filepath
class cl_ap(Resource):
	def get(self, file_name):	   # if two files are same always return the first file
			filename = file_name
			global machines
			for k,v in machines.items():
				for m,n in v.items():   
					for i in n:
						if str(i) == str(filename):
							file_dir = str(m)
							port = v['port']
							dictn = {}
							dictn.update({str(i): str(file_dir)})
							dictn.update({'port':port})               
			print 'sent all info to go to file server from ds'		## sending {filename:filepath, port:port}		
			return jsonify(dictn)				
ds.add_resource(cl_ap, '/<string:file_name>')

#------------------------------------#
if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 8080)

