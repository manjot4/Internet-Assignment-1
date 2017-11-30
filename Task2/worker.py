from radon.cli import Config
from radon.cli.harvest import CCHarvester
from radon.complexity import cc_rank, SCORE
from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
#app = Flask(__name__)
#wrkr = Api(app)

token = 'c8930325aee5239b9eef195498282a6016de9621'
payload = {"access_token" : str(token), "recursive" : 1}
headers = {'Accept':'application/vnd.github.VERSION.raw'}
#addr = 'https://api.github.com/repos/manjot4/Internet-Assignment-1/git/blobs/bfd80d6d4ee503b1817fd30bd5311d40ea156573'
#filee = requests.get(str(addr), params = payload, headers = headers)
#data = filee.content

config = Config(
        exclude="",
        ignore="",
        order=SCORE,
        no_assert=True,
        show_closures=True,
        min='A',
        max='F',
    )
#filenames
i = 0

while(True):
	get_url = requests.get('http://0.0.0.0:8080/')
	get_url = get_url.text
	get_url = json.loads(get_url)
	get_url = get_url['file_url']

	if (str(get_url) == 'done'):
		break 
	# wroker has url, get data from web
	address = get_url
	filee = requests.get(str(address), params = payload, headers = headers)
	data = filee.content
	#print data
	i = i+1
	filename = '/Users/manjotsingh/desktop/data_files/file'+str(i)
	f = open(str(filename), "w+")
	f.write(data)   
	f.close()
	
	cc = 0
	h = CCHarvester([filename], config)._to_dicts()
	for m in h:
		for n in h[m]:
				#print n
			#length = length+1
			com = n['complexity']
			cc = cc + com


	avg_comp = float(cc) 
	print 'cc', cc

	return_value = {'cc' : avg_comp}

	sending = requests.post('http://0.0.0.0:8080/', json = return_value)
	status = sending.text
	status = json.loads(status)
	status = status['received']
	print 'status :', status


print 'finished'









