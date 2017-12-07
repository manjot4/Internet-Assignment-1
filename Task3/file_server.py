from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
fs = Api(app)


# for now format -> {file_direc : {filename :{ version : path to file}, second file ..}, second direc..}
# for database, ask doubt...
file_direcs = {
	'files' : {'first.txt' : {'1' : '/Users/manjotsingh/desktop/files/first.txt'}, 'second.txt' : {'1': '/Users/manjotsingh/desktop/files/second.txt'}}, 
	'files1': {'first.txt' : {'1': '/Users/manjotsingh/desktop/files1/first.txt'}, 'second1.txt' : {'1': '/Users/manjotsingh/desktop/files1/second1.txt'}}
}

#file_direc = {
#	'first.txt': {0:'/Users/manjotsingh/desktop/files/first.txt'},
#	'second.txt': {0:'/Users/manjotsingh/desktop/files/second.txt'}
#}


#class name(Resource):

class file_s(Resource):
	def get(self, file_name):
		parser = reqparse.RequestParser()
		parser.add_argument('file_info', location = 'json')
		args = parser.parse_args()
		file_dir = args['file_info']
		filename = str(file_name)
		# have filename and filedirec....
		#have to get filepath
		for k,v in file_direcs.items():
			if str(k) == str(file_dir):
				for m,n in v.items():
					if str(m) == str(filename):
						for a,b in n.items():
							filepath = str(b)
		f = open(str(filepath), 'r')
		data = f.read()
		f.close()
		#print 'read all file'
		return {'file_data' : data}

		## client proxy itself gives the filepath 
	def post(self, file_name):
		filename = file_name
		parser = reqparse.RequestParser()
		parser.add_argument('file_info', location = 'json')
		parser.add_argument('summary', location = 'json')
		args = parser.parse_args()
		file_dir = args['file_info']	
		summary = args['summary']
		for k,v in file_direcs.items():
			if str(k) == str(file_dir):
				for m,n in v.items():
					if str(m) == str(filename):
						for a,b in n.items():
							filepath = str(b)
		## appending the file
		f = open(str(filepath), 'a')
		f.write(str(summary))
		f.close()
		print 'writing done'

		# do change the version of the file...
		## for now
		#for k,v in file_direc.items():
		#	if str(k) == str(filename):
		#		for i in v:
		#			i = i+1
		return {'writing':'successful'}

fs.add_resource(file_s, '/<string:file_name>')


# as soon as client wakes up, it gets machine id from direc server
def getmachineid():
	params = {'machine_id':'hello', 'port':8081, 'host':'0.0.0.0'}
	response = requests.get('http://0.0.0.0:8080/', json = params)
	response = response.text
	response = json.loads(response)
	machine_id = response['machine_id']
	print 'machine_id', machine_id
	# gets the machine id
	## sending the list of files for mapping to direc server

	#files = {}  ## files sent to dir_ser
	#for k,v in file_direcs.items():
	#	for i in v:
	#		#filee = {str(k) : v[i]}
	#		filee = {str(k) : str(i)}
	#		files.update(filee)
	#print 'sending files to directory server'   #new - {filedirec : filename} ,...., old#{filename: filepath, filename:filepath, ...}		
	#print 'files being sent:', files
	files = {}  ## files sent to dir_ser
	for k,v in file_direcs.items():
		files[str(k)] = [str(i) for i in v]    # {file irec : ['first.txt', ], file_direc : []}
	print 'sending files to directory server'   
	print 'files being sent:', files
	posting = requests.post('http://0.0.0.0:8080/'+str(machine_id), json = files)  # sending files with machine_id
	posting = posting.text
	posting = json.loads(posting)
	status = posting['data files_ds']
	print 'status:', status

	## sending same things to lock server as well
	print 'sending files to lock server'
	posting = requests.post('http://0.0.0.0:8082/'+str(machine_id), json = files)
	posting = posting.text
	posting = json.loads(posting)
	status = posting['data files_ls']
	print 'status:', status
	#return 		



#fs.add_resource(file_s, '/files/<file_name>')

if __name__ == '__main__':
	getmachineid()
	print 'file_direc', file_direcs
	app.run(debug=True, port = 8081, host = '0.0.0.0')
	## file server wakes up, goes to dir server for a machine id and when it gets, gives dir a list of files..
	#mach_id_dir = machine_id




