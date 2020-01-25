#!/usr/bin/python3
import os
import subprocess
cmd = "cat /proc/version | grep -o 'Debian\|Centos' -m 1"
version = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
version1 = version.communicate()[0]
if version1==b'Debian\nDebian\n':
	a='/var/log/syslog'
	b='syslog'
else:
	a='/var/log/dmesg'
	b='linux_logs'


def splunkconfigure():
	try:
		if not os.path.exists("splunkforwarder"):
			os.system("rm -rf splunkforwarder >/dev/null")
			os.system("tar -xzf u* >/dev/null")
			os.system("./splunkforwarder/bin/splunk start --accept-license --answer-yes --auto-ports --seed-passwd Password@123 >/dev/null 2>&1")
			os.system("./splunkforwarder/bin/splunk enable boot-start >/dev/null")
			os.system("./splunkforwarder/bin/splunk add forward-server 192.168.10.155:9997 -auth admin:Password@123 >/dev/null")
			os.system("./splunkforwarder/bin/splunk add monitor "+a+" -sourcetype "+b+" >/dev/null")
			os.system("./splunkforwarder/bin/splunk list forward-server >/dev/null")
			os.system("./splunkforwarder/bin/splunk set deploy-poll 192.168.10.155:9000 >/dev/null")
			with open("splunkforwarder/etc/system/local/inputs.conf", "a") as myfile:
				myfile.write("[monitor://"+a+"]\nsourcetype="+b)
			os.system("./splunkforwarder/bin/splunk restart >/dev/null")
			return "DONE"
		else:
			return "ALREADY"
	except:
		return "ERROR"


