from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
ds = Api(app)


machines = {}
id = 0
host = 0
port = 0

## giving client the machine id
class fs_id(Resource):
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

## udating his list of files
class fs_post(Resource):
	def post(self, machine_id):
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
		#dictn = {}
		#for i in response:
		#	data = response[str(i)]
		#	info = {str(i) : str(data)}
		#	dictn.update(info)
		#global host
		#global port	
		#dictn.update({'host':str(host)})
		#dictn.update({'port':port})
		#name = str(machine_id)
		#final_info = { name : dictn}
		#machines.update(final_info)
		#print machines
			#print 'file_direc1', file_direc1  ## create a direc with a name
		return {'data files_ds' : 'received'}
ds.add_resource(fs_post, '/<int:machine_id>')		

## receiving name of file and giving back port, ip, and filepath
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
							dictn.update({'port':port})               # full looping   
			#for k,v in machines.items():
			#	for i in v:    
			#		if str(i) == str(filename):
			#			## create all info that we'll be sending to client
			#			filepath = v[str(i)]
			#			host = v['port']
			#			dictn = {}
			#			info = {str(i):str(filepath)}
			#			dictn.update(info)
			#			dictn.update({'port':port})
			print 'sent all info to go to file server'		## sending {filename:filepath, port:port}		
			return jsonify(dictn)				



ds.add_resource(cl_ap, '/<string:file_name>')


if __name__ == '__main__':
	app.run(debug=True, host = '0.0.0.0', port = 8080)

