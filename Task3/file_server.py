# Name - Manjot Singh
# Student_Id - 16338467
# Program - file_server.py
#-----------------------#
from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
fs = Api(app)
#------------------------#

# filedirectories from my own machine 
file_direcs = {
	'files' : {'first.txt' : {'1' : 'files/first.txt'}, 'second.txt' : {'1': 'files/second.txt'}}, 
	'files1': {'first.txt' : {'1': 'files1/first.txt'}, 'second1.txt' : {'1': 'files1/second1.txt'}}
}

# if file exists in cache, client_proxy comes in everytime to make sure about the version of file.
# if same, reads from local cache
# if not, reads remotely.
class file_status(Resource):
	# client_proxy comes with its own version of file 
	# if version is same file server returns status as same.
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('file_info', location = 'json')
		parser.add_argument('filename', location = 'json')
		parser.add_argument('version', location = 'json')
		args = parser.parse_args()
		file_dir = args['file_info']
		filename = args['filename']
		version = args['version']
		# get the version which file server has
		for k,v in file_direcs.items():
			for m,n in v.items():
				if str(m) == str(filename):
					for i in n:
						if str(i) == str(version):
							return {'status' : 'same'}
						return {'status' : 'not same'}

fs.add_resource(file_status, '/')

# client_proxy comes here for first time to read/get the file remotely
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
							# get the version of that file as well
							version = a
							# get the filepath
							filepath = str(b)
		f = open(str(filepath), 'r')
		data = f.read()
		f.close()
		return {'file_data' : data, 'version' : version}

# client_proxy comes here to overwrite/append to a file
# comes in with what it has to write
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
							ver = a
							filepath = str(b)
							a = str(int(a)+1)
							n[str(a)] = n.pop(str(ver))
		#print 'filepath', filepath
		print 'filedir', file_direcs
		## appending the file
		f = open(str(filepath), 'a')
		f.write(str(summary))
		f.close()
		print 'writing done'
		return {'writing':'successful'} # returns status if writing is successful

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

# -----------------------------------------#
if __name__ == '__main__':
	# AT first gets machine od from dir server and then from lock server
	# regiters with both of them
	getmachineid()
	print 'file_direc', file_direcs
	app.run( port = 8081, host = '0.0.0.0')



##########END OF CODE#################

