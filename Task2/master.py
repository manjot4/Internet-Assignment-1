

# just need to get one worker connect to master and get one file at a time and return avg cc of that, and master can add that all.
# then try to incorporate multiple workers trying to get job and return results....


from flask import Flask, jsonify, request
import requests, json
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
ms = Api(app)

## to access 5000 files from my repo

payload = {"acess_token" : str(token), "recursive" : 1} # recursive

sha_lists = []


count = 0
#newtrees = {}
#trees = {}      #trees: {sha number : all details related to tree}
                    # in some trees, it mey have all files or it may have folders//
                    # which have folders will have type = tree...

def tree_details():
    trees = {}
    # getting all url's
    commits_address = 'https://api.github.com/repos/manjot4/Internet-Assignment-1/commits'
    r = requests.get(str(commits_address), params = payload).json() # returns all commits
    # since there are 19 commits at this time, getting all 19 sha's
    for commit in r:
        if 'sha' in commit:
            sha = commit['sha']
            sha_lists.append(sha) # storing all my sha's
            # getting all files at that commit
            commit_address = 'https://api.github.com/repos/manjot4/Internet-Assignment-1/git/trees/'+str(sha)
            response = requests.get(str(commit_address), params = payload).json()
            if 'tree' in response:
                tree_data = []
                for i in response['tree']:
                    tree_data.append(i)   # all files at that point in repo..//eg: task3, chatserver and files in them...
                    trees[sha] = tree_data
    return trees


def get_all_files():
    newtrees = {}
    trees = tree_details()
    for details in trees:   # details sha of commit
        finalsha = []     # final sha will have all details of files
        for i in trees[details]:
            if i['type'] != 'tree':
                finalsha.append(i)   
        newtrees[details] = finalsha
    return newtrees    



def get_all_url():
    file_urls = [] # contains all url's of all files
   # newtrees = {}
    allfiles = get_all_files()
    for sha in allfiles:   # i -> sha
        for filee in allfiles[sha]: #j -> all files at that time
            file_url = filee['url']
            file_urls.append(file_url)
            global count
            count = count + 1
            #print filee['url']
    return file_urls


#for i in files:
 #   print i
  #  print '---'
#print 'total files\n', count


#files = get_all_url()




cyclocomp = 0.0
num = 0
def add_cyclo(cc):
    global cyclocomp
    cyclocomp = cyclocomp + float(cc)

files = get_all_url()
number = len(files)

class ws(Resource):
    def get(self):  # wrong
        global number
        global num
        num = num + 1
        print 'num', num
        global cyclocomp
        print 'cyclo', cyclocomp 
        print 'hello'
        #global num
        url = files[number-1]
        number = number-1
        if number < 0:
            return {'file_url':'done'}
        else:
            return {'file_url': str(url)}   ## worker is given file url ... 
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cc', location = 'json')
        args = parser.parse_args()
        cc =  args['cc'] # return {'cc': value}
        print 'cc', cc
        add_cyclo(cc)
        #global cyclocomp
        
        return {'received' : 'thanks'}


ms.add_resource(ws, '/')



if __name__ == '__main__':
    
    app.run(debug=True, port = 8080, host = '0.0.0.0')
