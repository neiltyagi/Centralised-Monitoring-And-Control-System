#!/bin/bash

a=$(awk -F= '/^NAME/{print $2}' /etc/os-release)
b='"Debian GNU/Linux"'

if [ "$a" == "$b" ]; then
	apt update
	apt install python3 gcc python3-dev python3-pip -y

else
	yum repolist
	yum install python3 gcc python3-devel python3-pip -y

fi



pip3 install setuptools
pip3 install colorama
pip3 install prettytable
pip3 install psutil
pip3 install  python-crontab

