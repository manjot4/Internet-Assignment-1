import client_proxy
import sys

if __name__ == '__main__':
	print "Choose an Option:\n1. Read File\t2. Write File"
	option = raw_input('Enter a number: ')
	if option == str(1):
		filename =  raw_input('Enter name of file you wan to read\n')
		client_proxy.readfile(str(filename))  # passing filename to client proxy # client proxy will reply
		print 'file read'

	elif option == str(2):
		filename = raw_input('Enter name of file you want to write\n')
		content =  raw_input('Type to content to write\n')
		print 'content : \n', str(content)
		client_proxy.writefile(str(filename), str(content)) # client proxy will reply
		print 'written'
		
	else:
		print 'Type Error:'	
		# will loop back afterwards	