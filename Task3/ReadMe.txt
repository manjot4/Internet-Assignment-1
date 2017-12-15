Task - 3 
Distributed File System

The system exhibits the following features:
1. Distributed Transparent File Access
2. Caching
3. Directory Service
4. Lock Service

All the things i.e. interaction between different services are implemented in restful web service. 

Distributed transparent file access includes client, client proxy and a file server. 

A client is any person who types on a his machine the name of the file that he/she wants to read or write. Client_proxy is a library which will do all the background thing to get this file format the remote server which is the file server.

A NFS service has been implemented in this file system. Only reading and writing operations can be performed. 
A client side proxy is implemented as a library that hides all access to the file system behind a simple language mechanism. 
Client wakes up, types in the name of the file that he/she wants to read/write. 
After that, client proxy takes care of everything. 
Also, the role of directory server comes into play now. 
Client proxy gets the name, goes to the the directory server with the filename, asks for the file directory in which the file is and also asks for which file server has the file, in a way gets the port number of that server.
Then, it goes to file server with the file-directory name and tells it to return the file. The file server gives all the data of the file, which client proxy prints it on the screen or opens the file for the client, thus, ensuring that client only reads the file without going into any of this hassle. 
The file is read remotely, in a NFS system, but to the client it is like, that it is reading the file locally on his computer. 

File Server : 
As the file server wakes up, it registers itself with the directory server because there can be too many number of file servers present and connected with a single directory server and directory server needs to have record of every file server. Then, it gets a machine id from directory server and then it goes to the directory server with a list of files and their directory names,the machine id that it gets from directory server and with the port number on which it operates on. After doing that, it goes to lock server with its machine id, telling lock server to give a key to every file for locking operation. 
Also, it listens to the client, allows them to read a file or write a file. 
It stores the files in the format --> file directory, all filenames in a directory, filepaths and the latest version of the file. (all explained in code).  

Caching:
Actually, caching is also related in this. So, here it goes.
What happens is at first, client proxy creates a directory for cache files initially. client Proxy checks in its directory for the file, if the file is there, it goes to the directory server, asking information for the file server, then goes to file server, asking it about the version of the file, making sure that both of them have the latest version/ same version. If yes, client reads the file locally. If no, then client proxy makes sure that client reads the latest version of the file. To do this, it goes to file server and reads the latest file remotely and stores the new version of the file locally, doing caching.And also, if the file is not in the cache directory, then client goes to file server after getting details from directory server asking to read the file, reads the file and client stores the file in a local directory, thus making it available for future reference. 

Locking Service : 

A lock server is implemented which makes sure that no two clients make write to a file simultaneously. For this, if a client has to write to a file, client proxy goes to a lock server, asking for write access. If the lock server has the key for that file, it gives it to that client, thus allowing him to make changes to a file/ in this any change is appended to a file. Then client proxy goes to file server, making that change to a file, writes to a file remotely. 
Then, file server updates the version of the file as the file is overwritten. 
If by this time, any client comes to a lock server asking for write access, it simply denies the access by saying come back later, basically it keeps the client pools over and over again. Client has to come back and check if the key is available in order to write to a same file. 
Now, after writing to a file, client returns back the key to the lock server making it available for other clients to use. 


Directory Server:
It only maps file servers(machine id's), file directories with files. Client proxy comes to directory service at first, it gives back port number, name of filedirectory in which the file is. If the file doesn't exist, it simply returns an error as directory server isn't able to find a file that client is looking for. It remains same throughout the program except for a new file server as it adds new files to it's directory, also, it is assumed that there is no deletion of files. But, if the new file server spawns up, directory server registers it, also updates its hash table which maps all the files. 

So, in the above program, two clients client 1 and client 2 have been used to do all the experimentation. Two fileservers have been used thus ensuring that directory and lock server can handle any number of files servers. Four file directories with 2 files in each have been used for experimentation. 

Requirements
flask
flask-restful
json
requests
os
pathlib, path

Also, file directories which contains the files on which experimentation has been done are also added.


To run the program:
1. Start the directory and lock servers at first.
2. Then start two file servers using script.sh, or if anyone wants to play with one fileserver, can use either fileserver.py or fileserver2.py
3. Then start the client, it will ask for whether to read or write to a file. Choose an option and then type the name of the file. If anyone goes for write, it will also ask for what to write.

 



 