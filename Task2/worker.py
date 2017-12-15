# Name - Manjot Singh
# Student_Id - 16338467
# Program - Worker.py
#-----------------------#
# libraries stuff..
from radon.cli import Config
from radon.cli.harvest import CCHarvester
from radon.complexity import cc_rank, SCORE
from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
import os

# -----------------------#

#Token to access 5000 files, otherwise will have access to 60 files an hour
token =  # not given for security reasons
payload = {"access_token" : str(token), "recursive" : 1}
headers = {'Accept':'application/vnd.github.VERSION.raw'}

# for cyclomatic complexity
config = Config(
        exclude="",
        ignore="",
        order=SCORE,
        no_assert=True,
        show_closures=True,
        min='A',
        max='F',
    )

# directory for storing files if directory doesn't exist
filedirname = 'data_files'
if not os.path.exists(str(filedirname)):
	os.makedirs(str(filedirname))


# register with the master and get an id
get_id = requests.get('http://0.0.0.0:8080/')
get_id = json.loads(get_id.text)
get_id = get_id['id']
print 'get_id', get_id
print 'worker'+str(get_id)+ 'starting its jobs'

#filenames
i = 0

# worker comes in a loop after getting an id.
# gets all jobs that master has to offer to it.
while(True):
	# goes to master asking for jobs
	get_url = requests.get('http://0.0.0.0:8080/'+str(get_id))
	get_url = get_url.text
	get_url = json.loads(get_url)
	get_url = get_url['file_url']

	# if it gets done in response, it means master is out of jobs.
	if (str(get_url) == 'done'):
		break 

	# wroker has url, get data from web
	address = get_url
	filee = requests.get(str(address), params = payload, headers = headers)
	data = filee.content
	#saves data into a file
	i = i+1
	filename = str(filedirname)+'/'+str(i)+'.py'
	f = open(str(filename), "w+")
	f.write(data)   
	f.close()
	
	# process for getting avg cyclomatic complexity
	cc = 0
	lent = 1
	h = CCHarvester([filename], config)._to_dicts()
	if len(h) == 0:
		cc = 0
	else:
		for m in h:
			for n in h[m]:	
				lent = lent + 1		
				try:
					com = n['complexity']
					cc = cc + com
				except:
					cc = 0	
	avg_comp = float(cc) / float(lent)
	print 'cc', avg_comp

	return_value = {'cc' : avg_comp}

# worker gives back its job to master
	sending = requests.post('http://0.0.0.0:8080/'+str(get_id), json = return_value)
	status = sending.text
	status = json.loads(status)
	status = status['received']
	print 'status :', status

# after doing all jobs, worker returns back its id to master
sending = requests.post('http://0.0.0.0:8080/', json = {'id': str(get_id)})
sending = json.loads(sending.text)
status = sending['status']
print status
print 'worker'+str(get_id)+ 'finished'

####END OF CODE##############







