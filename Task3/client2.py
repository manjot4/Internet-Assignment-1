import client_proxy
import sys

if __name__ == '__main__':
	while True:
		print "Choose an Option:\n1. Read File\t2. Write File"
		option = raw_input('Enter a number: ')
		if option == str(1):
			filename =  raw_input('Enter name of file you wan to read\n')
			client_proxy.readfile(str(filename), str(2))  # passing filename to client proxy # client proxy will reply printing the data
			print 'file read'

		elif option == str(2):
			filename = raw_input('Enter name of file you want to write\n')
			client_proxy.writefile(str(filename), str(2)) # client proxy will reply asking for content to write
			print 'written'

		elif option == str(0):
			print "thanks"
			break

		else:
			print 'Type Error:'
				