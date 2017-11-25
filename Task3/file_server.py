from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
fs = Api(app)


file_direc = {
	'first.txt': {0:'/Users/manjotsingh/desktop/files/first.txt'},
	'second.txt': {0:'/Users/manjotsingh/desktop/files/second.txt'}
}


#class name(Resource):

class file_s(Resource):
	def get(self, file_name):
		parser = reqparse.RequestParser()
		parser.add_argument('file', location = 'json')
		args = parser.parse_args()
		filepath = args['file']
		filename = str(file_name)
		#for k,v in file_direc.items():
		#	if str(k) == filename:
		#		filepath =
		f = open(str(filepath), 'r')
		data = f.read()
		f.close()
		return {'file_data' : data}
	def put(self, file_name):
		pass	
		## will be given full modified file, open the same file, replace its data with new data
		## make sure everyone who has those  files have their updated version....
fs.add_resource(file_s, '/file_name')

def getmachineid():
	params = {'machine_id':'hello', 'port':8081, 'host':'0.0.0.0'}
	response = requests.get('http://0.0.0.0:8080/', json = params)
	response = response.text
	response = json.loads(response)
	machine_id = response['machine_id']
	print 'machine_id', machine_id
	## sending the list of files for mapping
	files = {}  ## files sent to dir_ser
	for k,v in file_direc.items():
		for i in v:
			filee = {str(k) : v[i]}
			files.update(filee)
	print 'files being sent:', files
	posting = requests.post('http://0.0.0.0:8080/'+str(machine_id), json = files)
	posting = posting.text
	posting = json.loads(posting)
	status = posting['data files']
	print 'status:', status
	#return 		



fs.add_resource(file_s, '/files/<file_name>')

if __name__ == '__main__':
	getmachineid()
	print 'file_direc', file_direc
	app.run(debug=True, port = 8081, host = '0.0.0.0')
	## file server wakes up, goes to dir server for a machine id and when it gets, gives dir a list of files..
	#mach_id_dir = machine_id




