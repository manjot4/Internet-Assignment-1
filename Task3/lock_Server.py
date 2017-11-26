from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
ls = Api(app)

## managing different file servers
machines = {}   ##{1:{first.txt :1, second.txt:1}, 2: ..}


## lock key given to every file initially.
key = 1
## make interaction between ls and file server...
## file server comes with machine id, tells ls to give keys to all files
class ls_fs(Resource):
	def post(self, machine_id):
		response = request.json
		dictn = {}
		for i in response:
			data = response[str(i)]
			info = {str(i) : key}
			dictn.update(info)
		name = str(machine_id)
		final_info = { name : dictn}
		machines.update(final_info)
		print machines
		return {'data files_ls' : 'received'}
ls.add_resource(ls_fs, '/<int:machine_id>')	

## possibility that both machines have two files of same names, so all comparison is wrong

class cp_ls(Resource):
	def get(self, file_name):
		filename = file_name
		for k,v in machines.items():
			for i in v:
				if str(i) == str(filename):
					if v[str(i)] == 1:
						v[str(i)] = 0 #making 1 -> 0
						
						return {'status' : 'sent'}
					else:
						return {'status' : 'not sent'}		



ls.add_resource(cp_ls, '/<string:file_name>')

if __name__ == '__main__':
	app.run(debug=True, host = '0.0.0.0', port = 8082)
