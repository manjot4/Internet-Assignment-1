# Name - Manjot Singh
# Student_Id - 16338467
# Program - Master.py
#-----------------------#
# importing libraries
from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
import time
app = Flask(__name__)
ms = Api(app)
#-----------------------#

# Token to access 5000 files
token = # not given for security reasons
payload = {"access_token" : str(token), "recursive" : 1} 

# list stores all sha keys
sha_lists = []

# worker id
id = 0 

def tree_details():

    trees = {}
    commits_address = 'https://api.github.com/repos/manjot4/Internet-Assignment-1/commits'
    r = requests.get(str(commits_address), params = payload).json() # returns all commits
    for commit in r:
        if 'sha' in commit:
            sha = commit['sha']
            sha_lists.append(sha)   # all sha keys
            commit_address = 'https://api.github.com/repos/manjot4/Internet-Assignment-1/git/trees/'+str(sha)
            response = requests.get(str(commit_address), params = payload).json()
            if 'tree' in response:
                tree_data = []
                for i in response['tree']:
                    tree_data.append(i)   
                    trees[sha] = tree_data  
    return trees

def get_all_files():
    newtrees = {}
    trees = tree_details()
    for details in trees:   
        finalsha = []     
        for i in trees[details]:
            if i['type'] != 'tree':
                finalsha.append(i)   
        newtrees[details] = finalsha
    return newtrees    

# make sures it matches only python files extensions.
def pyth_file(filename):
    if str(filename).endswith('.py'):
        return True
    else:
        return False    

# to get url of all commits
def get_all_url():
    file_urls = [] 
    allfiles = get_all_files()
    for sha in allfiles:   
        for filee in allfiles[sha]: 
            # make sure it is a python file...
            if filee['type'] == 'blob' and pyth_file(filee['path']):
                file_url = filee['url']
            file_urls.append(file_url)
    return file_urls


number = 0

# cyclomatic Complexity
cyclocomp = 0.0

# Cyclomatic Complexity adds after every worker submit it's job
def add_cyclo(cc):
    global cyclocomp
    cyclocomp = cyclocomp + float(cc)

# list to store every worker's return ids    
return_ids = []

# worker comes, gets jobs and post back back results
# every worker comes with its worker id
class ws(Resource):
    #gives url to worker
    def get(self, worker_id):  
        global files
        global number
        global cyclocomp
        print 'number', number 
        print 'cyclo', cyclocomp 
        number = number+1
        if number >= len(files):
            print 'final cyclomatic complexity value', cyclocomp/len(files)
            return {'file_url':'done'}
        else:
            url = files[number]
            return {'file_url': str(url)}   # worker being given the file url/job

     # receives cyclomatic complexity       
    def post(self, worker_id):
        parser = reqparse.RequestParser()
        parser.add_argument('cc', location = 'json')
        args = parser.parse_args()
        cc =  args['cc'] 
        print 'cc', cc
        add_cyclo(cc)
        return {'received' : 'thanks'}

ms.add_resource(ws, '/<int:worker_id>')


# worker comes asks for id and return back the same id
class rw(Resource):
    # master gives worker its id/registers worker
    def get(self):
        global id
        id = id+1
        return {'id' : id}

# master gets back all id's and on getting back last id decides to stop the time 
    def post(self):
        global id
        parser = reqparse.RequestParser()
        parser.add_argument('id', location = 'json')
        args = parser.parse_args()
        return_id =  args['id']
        print 'return_id', return_id 
        return_ids.append(return_id)
        if len(return_ids) == id:
            endtime = time.time()
            print 'time taken:', (endtime - start_time)
        return {'status' : 'thanks pal'}   
ms.add_resource(rw, '/')


#-----------------------------------------------------------#
#program starts here
if __name__ == '__main__':
    # get url of every file on git
    files = get_all_url()
    # starting the time here
    start_time = time.time()
    print 'start_time', start_time
    app.run(port = 8080, host = '0.0.0.0')
  
    

####END OF CODE##############