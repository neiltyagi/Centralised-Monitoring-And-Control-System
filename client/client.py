#!/usr/bin/python3
import socket
import subprocess
import os
import time
import platform
import tempfile
import shutil
import psutil
from datetime import datetime
from crontab import CronTab
import ciscontrols
import splunkenable


IPADDRESS="EDIT YOUR IP HERE WITHIN THE QUOTES"
PORT=8080 #DEFAULT



global s


def connect():
    global s
    while True:

        x=5
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(('192.168.10.155',8080))
            x=0

        except:
            time.sleep(5)

        if x == 0 :
            break



def transferupload(s,command):
	upload,path=command.split('*')
	fpath=os.getcwd()+"/"
	fpath += os.path.basename(path)
	f=open(fpath,'w')
	bits=s.recv(1024).decode()
	while True:
		f.write(bits)
		bits=s.recv(1024).decode()
		if bits.endswith("DONE"):
			f.write(bits.strip("DONE"))
			f.close()
			break



def transfergrab(s,path):
	if os.path.exists(path):
		if os.path.isfile(path):
			f=open(path,'r')
			f.seek(0)
			packet=f.read(1024)
			while packet:
				s.send(packet.encode())
				packet=f.read(1024)
			s.send(("DONE").encode())
			f.close()
		else:
			s.send("DIR".encode())
	else:
		msg="The File Doesn't Exist"
		s.send(msg.encode())




def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor




def connection():
	
	global s

	while True:

		command=s.recv(1024)
		command=command.decode()

		if 'grab' in command:
			grab,path=command.split('*')
			transfergrab(s,path)


		elif 'upload' in command:
			transferupload(s,command)


		elif 'cd' in command:
			code,directory = command.split ('*')
			try:
				os.chdir(directory)
				s.send(("[+] CWD Is " + os.getcwd()).encode())
			except:
				s.send("[-] PATH NOT FOUND".encode())

		elif 'shell' in command:
			shell,query = command.split('*')
			query=query.split()
			try:
				cmd=subprocess.Popen(query,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				stdout,stderr=cmd.communicate()
				if stdout:
					s.send(stdout)
					s.send(("DONE").encode())
				elif stderr:
					s.send(stderr)
					s.send(("DONE").encode())
				else:
					s.send(("DONE").encode())
			except:
				s.send("COMMAND_NOT_FOUND".encode())

		elif 'SLEEP' in command: 
			s.close()
			time.sleep(16)
			break

		elif 'os' in command:
			uname=platform.uname()
			a=uname.system+"$"+uname.node+"$"+uname.machine+"$"+uname.version
			s.send(a.encode())

		elif 'status' in command:
			uname=platform.uname()
			boot_time_timestamp = psutil.boot_time()
			bt = datetime.fromtimestamp(boot_time_timestamp)
			svmem = psutil.virtual_memory()
			swap = psutil.swap_memory()
			cpufreq = psutil.cpu_freq()
			bootdate=str(bt.year)+"-"+str(bt.month)+"-"+str(bt.day)
			boottime=str(bt.hour)+":"+str(bt.minute)+":"+str(bt.second)
			tm=str(get_size(svmem.total))
			am=str(get_size(svmem.available))
			um=str(get_size(svmem.used))
			perm=str(svmem.percent)+"%"
			ts=str(get_size(swap.total))
			fs=str(get_size(swap.free))
			cpuf=str(cpufreq.current)+"Mhz"
			tcpu=str(psutil.cpu_percent())+"%"
			data=uname.system+"$"+uname.node+"$"+uname.machine+"$"+uname.version+"$"+bootdate+"$"+boottime+"$"+tm+"$"+am+"$"+um+"$"+perm+"$"+ts+"$"+fs+"$"+cpuf+"$"+tcpu
			s.send(data.encode())


		elif 'cischeck' in command:
			cischeck(s)

		elif 'cisenable' in command:
			cisenable(s)
		elif 'message' in command:
			message(s,command)

		elif 'splunkenable' in command:
			splunkenableremote(s,command)

def splunkenableremote(s,command):
	status=splunkenable.splunkconfigure()
	if status=='DONE':
		s.send("DONE".encode())
	elif status=='ALREADY':
		s.send('ALREADY'.encode())
	elif status=='ERROR':
		s.send('ERROR'.encode())





def message(s,command):
	message,cmd=command.split("*")
	if os.system(cmd) == 0 :
		s.send("DONE".encode())
	else:
		s.send("ERROR".encode())


def cisenable(s):
	path="/admin/after.txt"
	if ciscontrols.enabled() and os.path.exists(path):
		transfergrab(s,path)
		os.remove(path)
	else:
		s.send("ERROR".encode())

def cischeck(s):
        path="/admin/before.txt"
        if ciscontrols.status() and os.path.exists(path):
                transfergrab(s,path)
                os.remove(path)
        else:
                s.send("ERROR".encode())




def persistence():
	destination="/admin/client.py"
	if not os.path.exists(destination):
		os.mkdir("/admin")
		source1=os.getcwd()+"/"+"client.py"
		source2=os.getcwd()+"/"+"ciscontrols.py"
		source3=os.getcwd()+"/"+"splunkenable.py"
		source4=os.getcwd()+"/"+"universalforwarder"
		shutil.copyfile(source1, destination)
		shutil.copyfile(source2, "/admin/ciscontrols.py")
		shutil.copyfile(source3, "/admin/splunkenable.py")
		shutil.copyfile(source4, "/admin/universalforwarder")
		cron = CronTab(user='root')
		job = cron.new(command='/usr/bin/python3 /admin/client.py &')
		job.every_reboot()
		cron.write()














#persistence()


while True:
	global s
	connect()
	connection()
