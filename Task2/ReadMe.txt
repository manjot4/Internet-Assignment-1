Task-2

Rest Service - Calculating Cyclomatic Complexity with master-worker method.

Overall Working : 
Master - Woker pattern is used to get the cyclomatic complexity of a code using restful service. When the master wakes up, it gets the list of commits from a particular reposiory and from there, file blobs url from the GitHub using GitHub api. Then the worker/workers depending upon how many nodes one wants to work with comes in registering themselves with the master/ gets an id and after it gets an id, it starts taking work from the master. Master will only give the work if the worker has an id. No work will be given to worker without an id. Worker only shuts off when the master is left with no jobs. Otherwise, it will keep coming in asking for more and more jobs.  
It is kind of like a work stealing pattern among all workers. Also, cyclomatic complexity is calculated only on python files.
 

Master:

Master starts off by getting all file url's from the GitHub. For this, I have used the token which allows 5000 requests an hour. It could also work without token, but the access will be 60 files an hour. So, first get all SHA's/commits and then, from that get all information about trees that is status of the repository at that particular commit. From there, one can get all the file urls. 
If one doesn't have access to a GitHub token, then from the code snippet, 
'requests.get(str(commits_address), params = payload).json()'  
params = payload argument can be removed. Then, one will just have access to 60 requests an hour.  
Now, master starts the time as workers start to come in.
After that, workers start coming in, master gives them an id, then gives each worker the job only when they ask for it. When worker is finished with the job, it returns back the job results to the master, which in this case is average cyclomatic complexity. The master receives it, adds it up every time and then at end takes the average of them. 
When the master gets back all the id's, or when every worker finishes it's job or there are no jobs left, then master records the time. So, both the times i.e. (endtime-starttime) are subtracted to get the total time in which overall work is done.
 

Worker:

On the worker side, a file directory is made if it doesn't exist. This file directory stores all python files taken up from the git for which the worker calculates the cyclomatic complexity. 
In the beginning, worker registers itself with the master.
Once it gets an id, it runs in a while loop. It only comes out of the loop when the master says that it is finished or out of jobs. But until that, it gets the job url, saves the file, calculates the average cyclomatic complexity for it and returns the result back to master and then goes back again to get another job.
After finishing, it returns it's id back to the master.

Graph:

Total of 7 workers are used to get the job done i.e to get the cyclomatic complexity on a full repository and result which is time taken by them to do the job is recorded. The same process is repeated with 6,5,4,3,2,1 number of workers as well. 
So, graph has been made between time taken to complete the process and the number of workers and can be found in Graph.png. The graph tells us that the time taken will decrease as the number of workers to complete the process increases, but only up to certain threshold point, after that time taken will again increase if we again increase the number of workers as too many workers will create mess. 

Requirements:
flask
flask-restful
requests
json
time
re, match

Repository:
This folder(task2) contains Readme.txt, worker.py, script.sh, master.py, graph.png files.

Launch the program:
#The repository used for this process is my own repository.
# 'manjot4/Internet-Assignment-1'

To run the files, please follow the process:
1. Run the master.py first and when the time starts, go to step 2.
2. Run the script.sh but in the script please specify, how many workers one wants to spawn, mention the number of python files.
3. Then, in the results one will find the time taken and average cyclomatic complexity of a repository. 


