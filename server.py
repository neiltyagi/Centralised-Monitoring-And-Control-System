#!/usr/bin/python3
import socket
import os
from threading import Thread
from prettytable import PrettyTable
from colorama import Fore, Style
import time
import sys



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print ("Correct usage: script <IP address> <port number>")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.bind((IP_address, Port))
server.listen(50)



list_of_clientsocket = []
list_of_clientaddr = []

flag=True


bottable = PrettyTable(['INDEX','IP','PORT','OS','HOSTNAME','ARCH','VERSION'])



def session(conn):

	print ("\n \n")
	print ("==========================")
	print ("CONNECTED TO THE CLIENT")
	print ("==========================") 
	print (Fore.YELLOW)
	print ("PRESS HELP FOR INSTRUCTIONS")
	print (Style.RESET_ALL)
	print ("\n")

	while True:
		try:
			command=input("client>")
		except KeyboardInterrupt:
			quitsafely()

		if 'exit' in command:
			print ("\n BACK TO MOTHERSHIP \n")
			return

		elif 'grab*' in command:
			try:
				transfergrab(conn,command)
			except:
				conn.close()
				remove(conn)
				return
		elif 'upload*' in command:
			try:
				transferupload(conn,command)
			except:
				conn.close()
				remove(conn)
				return
		elif 'cd*' in command:
			conn.send(command.encode())
			shell=conn.recv(1024).decode()
			print (shell)

		elif 'shell*' in command:
			shellexec(conn,command)
		elif 'help' in command:
			helpbot()

		elif 'status' in command:
			try:
				clientstatus(conn,command)
			except:
				conn.close()
				remove(conn)
				return

		elif 'users' in command:
			try:
				userlist(conn)
			except:
				conn.close()
				remove(conn)
				return

		elif 'cischeck' in command:
			try:
				cischeck(conn,command)
			except:
				conn.close()
				remove(conn)


		elif 'cisenable' in command:
			try:
				cisenable(conn,command)
			except:
				conn.close()
				remove(conn)

		elif 'message' in command:
			message(conn,command)

		elif 'splunkenable' in command:
			splunkenable(conn,command)

		else:
			print("INVALID COMMAND PRESS HELP FOR MORE INFO")


def splunkenable(conn,command):
	conn.send(command.encode())
	print(Fore.YELLOW)
	print("[]Splunk is being configured on the remote client.Please wait...")
	print(Style.RESET_ALL)
	msg=conn.recv(1024).decode()

	if 'DONE' in msg:
		print(Fore.GREEN)
		print("[+]splunk enabled successfully")
		print(Style.RESET_ALL)
	elif 'ALREADY' in msg:
                print(Fore.YELLOW)
                print("[+]splunk Already Configured")
                print(Style.RESET_ALL)
	elif 'ERROR' in msg:
                print(Fore.RED)
                print("[-]Some Error occured at remote host")
                print(Style.RESET_ALL)




def shellexec(conn,command):
	shell,comm=command.split("*")
	if comm.startswith("cd"):
		print(Fore.YELLOW)
		print("[-] Use the cd*<path> directive for directory traversal")
		print(Style.RESET_ALL)
	else:
		try:
			conn.send(command.encode())
			shell=conn.recv(1024).decode()
		except:
			conn.close()
			remove(conn)
			return

		else:
			if shell.startswith("COMMAND_NOT_FOUND"):
				print("command not found")
			else:
				while True:
					print (shell)
					if shell.endswith("DONE") or not shell:
						break
					shell=conn.recv(1024).decode()


def message(conn,commad):
	print("List of current terminals connected to this machine")
	print("--------------------------")
	shellexec(conn,'shell*who')
	print("Enter Terminal no you wish to send message")
	print("Example tty1 tty2 etc")
	print("---------------------------------------")
	tty=input("terminal>")
	msg=input("enter message>")
	cmd="message*echo "+"'"+msg+"'"+" > "+"/dev/"+tty
	conn.send(cmd.encode())
	msg=conn.recv(1024).decode()
	if 'DONE' in msg:
		print(Fore.GREEN)
		print("[+]message successfully sent")
		print(Style.RESET_ALL)
	elif 'ERROR' in msg:
		print(Fore.RED)
		print("[-] Some error occured at remote host")
		print(Style.RESET_ALL)






def cisenable(conn,command):
        conn.send(command.encode())
        bits=conn.recv(1024).decode()
        if bits.startswith("ERROR"):
                print(Fore.RED)
                print("[-] Some error occured at remote host")
                print(Style.RESET_ALL)
        else:
                f=open("after.txt",'w')
                while True:
                        f.write(bits)
                        bits=conn.recv(1024).decode()
                        if bits.endswith("DONE"):
                                f.write(bits.strip("DONE"))
                                f.close()
                                break


                f=open("after.txt","r")
                lines=f.readlines()
                for line in lines:
                        print(line.strip("\n"))
                os.remove("after.txt")










def cischeck(conn,command):
	conn.send(command.encode())
	bits=conn.recv(1024).decode()
	if bits.startswith("ERROR"):
		print(Fore.RED)
		print("[-] Some error occured at remote host")
		print(Style.RESET_ALL)
	else:
		f=open("before.txt",'w')
		while True:
			f.write(bits)
			bits=conn.recv(1024).decode()
			if bits.endswith("DONE"):
				f.write(bits.strip("DONE"))
				f.close()
				break


		f=open("before.txt","r")
		lines=f.readlines()
		for line in lines:
			print(line.strip("\n"))
		os.remove("before.txt")






def userlist(conn):
	try:
		conn.send("grab*/etc/passwd".encode())
		path=os.getcwd()+'/'+'temppasswd'
		f=open(path,'w')
		bits=conn.recv(1024).decode()
		while True:
			f.write(bits)
			bits=conn.recv(1024).decode()
			if bits.endswith("DONE"):
				f.write(bits.strip("DONE"))
				f.close()
				break
	except:
		os.remove(path)
		return

	f=open(path,'r')
	line=f.readlines()
	usertable=PrettyTable(['Username','UID','HomeDirectory','Shell'])
	print("\n1. For System Users")
	print("2. For Normal Users")
	print("Any Key to go back")
	print("-----------------------")
	option=input("Option>")
	if option.isdigit():
		option=int(option)
	else:
		f.close()
		os.remove(path)
		return

	for i in line:
		a=i.split(":")
		a.pop(4)
		a.pop(3)
		a.pop(1)
		if option ==1:
			if int(a[1])<1000:
				usertable.add_row(a)
		if option ==2:
			if int(a[1])>=1000:
				usertable.add_row(a)
	if option == 1 or option == 2:
		print(usertable)
		f.close()
		os.remove(path)
	else:
		f.close()
		os.remove(path)
		return





def remove(connection):

    if connection in list_of_clientsocket:
        x=list_of_clientsocket.index(connection)
        list_of_clientsocket.pop(x)
        print(Fore.RED)
        print ("[-] client disconnected " + list_of_clientaddr[x][0] + "\n")
        print(Style.RESET_ALL)
        list_of_clientaddr.pop(x)




def mothership():
	global flag
	while True:
		try:
			command=input("<MotherNode>")
		except KeyboardInterrupt:
			quitsafely()

		if 'showclients' in command:
			x=showclients()
			while x != 0:
				x=showclients()



		elif "connect" in command:
			a,b=command.split(" ")
			b=int(b)
			if b<len(list_of_clientaddr):
				session(list_of_clientsocket[b])
			else:
				print(Fore.RED)
				print("[-]index out of range TRY AGAIN (indexing starts from 0)")
				print(Style.RESET_ALL)

		elif "exit" in command:
			quitsafely()
		elif "help" in command:
			helpmothership()

		else:
			print("Invalid Command Press help for more info")

def showclients():

	bottable.clear_rows()
	for x in range(len(list_of_clientsocket)):
		try:
			list_of_clientsocket[x].send('os'.encode())
			clientinfo=list_of_clientsocket[x].recv(1024)
			if not clientinfo:
				list_of_clientsocket[x].close()
				remove(list_of_clientsocket[x])
				return 1

		except:
				list_of_clientsocket[x].close()
				remove(list_of_clientsocket[x])
				return 1


		clientinfo=clientinfo.decode()
		clientinfo=clientinfo.split('$')
		table=[x,list_of_clientaddr[x][0],list_of_clientaddr[x][1]]
		table.extend(clientinfo)
		bottable.add_row(table)


	print ("CURRENTLY CONNECTED CLIENTS")
	print ("----------------------------")    
	print (bottable)
	return 0

def clientstatus(conn,command):
	conn.send(command.encode())
	data=conn.recv(1024)
	data=data.decode()
	data=data.split('$')
	osdetailslist=data[0:6]
	memorylist=data[6:10]
	swaplist=data[10:12]
	cpulist=data[12:14]
	osdetailstable = PrettyTable(['Os','Hostname','Arch','Version','Boot Date','Boot Time'])
	memorytable = PrettyTable(['Total Memory','Available Memory','Used Memory','Percent Use'])
	swaptable = PrettyTable(['Total Swap','Free Swap'])
	cputable = PrettyTable(['Current Clock Speed','CPU %'])

	osdetailstable.add_row(osdetailslist)
	memorytable.add_row(memorylist)
	swaptable.add_row(swaplist)
	cputable.add_row(cpulist)

	print("OS DETAILS")
	print(osdetailstable)
	print("MEMORY STATUS")
	print(memorytable)
	print("SWAP STATUS")
	print(swaptable)
	print("CPU STATUS")
	print(cputable)


def botconnect():

    global flag
    while flag:

        conn, addr = server.accept()
        list_of_clientsocket.append(conn)
        list_of_clientaddr.append(addr)
        if flag==True:
            print(Fore.GREEN)
            print("\n [+] incoming connection " + addr[0] + " connected")
            print(Style.RESET_ALL)


def transfergrab(conn,command):
	grab,path=command.split('*')
	if not path.startswith("/"):
                                print(Fore.YELLOW)
                                print("[-] Please specify the complete path")
                                print(Style.RESET_ALL)

	else:
		conn.send(command.encode())
		fpath=os.getcwd()+"/"
		fpath += os.path.basename(path)
		bits=conn.recv(1024).decode()
		if "The File Doesn't Exist" in bits:
			print(Fore.RED)
			print("[-]The File Doesn't Exist")   
			print(Style.RESET_ALL)
		elif "DIR" in bits:
			print(Fore.YELLOW)
			print("[-]Cannot grab a Directory")
			print(Style.RESET_ALL)
		elif "ERROR" in bits:
			print(Fore.RED)
			print("[-]Some error occured at remote host")
			print(Style.RESET_ALL)

		else:
			f=open(fpath,'w')
			while True:
					f.write(bits)
					bits=conn.recv(1024).decode()
					if bits.endswith("DONE"):
						f.write(bits.strip("DONE"))
						print(Fore.GREEN)
						print("[+]File Transfer Complete and saved at CWD")   
						print(Style.RESET_ALL)
						f.close()
						break




def transferupload(conn,command):
	print(Fore.YELLOW)
	print("[+] YOU HAVE INVOKED THE UPLOAD COMMAND")
	print(Style.RESET_ALL)
	upload,path=command.split('*')
	if os.path.exists(path):
		if os.path.isfile(path):
			conn.send(command.encode())
			print(Fore.BLUE)
			print("[+]UPLOADING")
			print(Style.RESET_ALL)
        
			f=open(path,'r')
			f.seek(0)
			packet=f.read(1024)
			while packet:
				conn.send(packet.encode())
				packet=f.read(1024)
			conn.send("DONE".encode())
			f.close()
			print(Fore.GREEN)
			print("[+]UPLOAD SUCCESSFULL")
			print(Style.RESET_ALL)
		else:
			print(Fore.YELLOW)
			print("[-]Cannot upload a directory")
			print(Style.RESET_ALL)
	else:
		print(Fore.RED)
		print("[-]The File Doesn't Exist")
		print(Style.RESET_ALL)
        
        
        
def quitsafely():
    global flag
    ans=input("\n ARE YOU SURE?(Y/N) ")
    if ans=='y' or ans=='Y':
        flag = False
        
        for conn in list_of_clientsocket:
            
            
            conn.send("SLEEP".encode())
            x=list_of_clientsocket.index(conn)
            print ("going to sleep "+list_of_clientaddr[x][0] )
            conn.close()
                
        print(Fore.GREEN)
        print("\n --------------------------------------------------------------------------")
        print("ALL BOTS ARE SLEEPING IT IS SAFE TO QUIT/EXIT NOW.")
        print("EXITING IN 5 SECONDS")
        print(" --------------------------------------------------------------------------")
        print(Style.RESET_ALL)
        
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((str(sys.argv[1]),int(sys.argv[2])))
        
        print(Fore.RED)
        for remaining in range(5, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
            sys.stdout.flush()
            time.sleep(1)
        print(Style.RESET_ALL)
        exit()
        sys.exit()
    else:
        return

def graphics():


	print("\n\n\n")
	print(Fore.GREEN)
	print('''		 ██████╗███╗   ███╗ ██████╗███████╗
		██╔════╝████╗ ████║██╔════╝██╔════╝
		██║     ██╔████╔██║██║     ███████╗
		██║     ██║╚██╔╝██║██║     ╚════██║
		╚██████╗██║ ╚═╝ ██║╚██████╗███████║
	 	╚═════╝╚═╝     ╚═╝ ╚═════╝╚══════╝
     		Centralised Monitoring And Control System
     		A framework Purely in Python''')
	print(Fore.YELLOW)
	print('''   	  ___   _      ___   _      ___   _      ___   _      ___   _
	 [(_)] |=|    [(_)] |=|    [(_)] |=|    [(_)] |=|    [(_)] |=|
	  '-`  |_|     '-`  |_|     '-`  |_|     '-`  |_|     '-`  |_|
	 /mmm/  /     /mmm/  /     /mmm/  /     /mmm/  /     /mmm/  /
	       |____________|____________|____________|____________|
	                             |            |            |
	                         ___  \_      ___  \_      ___  \_
	                        [(_)] |=|    [(_)] |=|    [(_)] |=|
	                         '-`  |_|     '-`  |_|     '-`  |_|
	                        /mmm/        /mmm/        /mmm/''')
	print("		Enter Help For Instructions")
	print(Style.RESET_ALL)
	print("\n \n \n  ")
def helpmothership():
    
    
    print("+----------------+--------------------------------------+")
    print("|     COMMAND    | DESCRIPTION                          |")
    print("+----------------+--------------------------------------+")
    print("| showclients    | display table of connected clients   |")
    print("+----------------+--------------------------------------+")
    print("| connect <index>| connect to bot at a specified index  |")
    print("+----------------+--------------------------------------+")
    print("| exit           |exit the application(bots go to sleep)|")
    print("+----------------+--------------------------------------+")
    print("| help           | see this table                       |")
    print("+----------------+--------------------------------------+")  
    print("\n")

def helpbot():
    
    print("+-------------------+--------------------------------------------------------+")
    print("|      COMMAND      | DESCRIPTION                                            |")
    print("+-------------------+--------------------------------------------------------+")
    print("|        exit       | back to mothership(stay connected to the remote host   |")
    print("+-------------------+--------------------------------------------------------+")
    print("|        help       | see this table                                         |")
    print("+-------------------+--------------------------------------------------------+")
    print("|        users      | get list of users on the remote host                   |")
    print("+-------------------+--------------------------------------------------------+")
    print("|  shell*<command>  | execute a shell command on remotehost                  |")
    print("+-------------------+--------------------------------------------------------+")
    print("|  grab*<file_name> | transfer a file from cwd of bot to cwd of mothernode   |")
    print("+-------------------+--------------------------------------------------------+")
    print("| upload*<filename> | transfer a file from cwd of mothership to cwd of client|")
    print("+-------------------+--------------------------------------------------------+")
    print("|     cd*<path>     | change cwd of bot                                      |")
    print("+-------------------+--------------------------------------------------------+")
    print("|     status        | get os memory and cpu statistics of remote client      |")
    print("+-------------------+--------------------------------------------------------+")
    print("|     cischeck      | get current cis complaint status of remote client      |")
    print("+-------------------+--------------------------------------------------------+")
    print("|     cisenable     | make remote system cis complaint                       |")
    print("+-------------------+--------------------------------------------------------+")
    print("|     message       | send message to the remote host                        |")
    print("+-------------------+--------------------------------------------------------+")







t1 = Thread(target = botconnect)

graphics()
t1.start()
mothership()






