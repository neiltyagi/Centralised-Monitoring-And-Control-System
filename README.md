# Centralised Monitoring And Control System 
A centralised server to manage and monitor remote clients.
A framework purely in python.

<img width="600" alt="logo" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/2.PNG">


# INTRODUCTION
----

Centralised Monitoring And Control System(CMCS) is the combination of a remote host handler(MotherNode) and a script(client) purely written in python that can make other computers slave (clients) of the MotherNode.The server script is named server.py and the client script must be administered on remote systems(clients).
The server provides the functionality of simultaneously handling and listening for multiple incoming socket connections.
The code base consists of four client side codes namely:

ciscontrols.py **This is for Checking and Implementing few CIS Compliance And Benchmarks.**

client.py **The Client-Side code to initiate a reverse TCP connection**

dependencyclient.sh **A bash script to check all the required dependencies(binaries) are installed or not**

splunkenable.py **To start splunk-forwarder on remote clients to monitor their logs in Splunk-UI**


>This has been made public that anyone can contribute to this project.


# REQUIREMENTS
----
The Program has been made and tested to work on Centos7 and DEBIAN 9




# FEATURES
----
- The Server can interact with one client while it is still listening for incoming connection from other clients.
- A low level client server model that does not trigger antivirus or firewalls.
- New connections are appended to a table that can be used later.
- The client script(agent) provides feature of persistence on platforms like centos or debian(adding a cronjob in crontab.)
- The script copies itself into the admin folder in the home directory and autoruns on reboot so that it works even if the original file is deleted by user.
- It **works over wan also** provided there is an ip connectivity between the MotherNode and the client.
- CIS Benchmarks that are applicable for the remote host can be listed and applied remotely.
- Splunk Forwarder can be configured on the remote host.
- Os,Memory and cpu statistics of the remote host can be monitored.
- List of Users (privileged and non-privileged ) present on the remote system can be viewed.
- Files can be transferred to and fro between server and client.
- Some commands that can be run on the clients are :-



|      COMMAND      | DESCRIPTION                                            |
|:-----------------:|--------------------------------------------------------|
|        exit       | back to mothership(stay connected to the bot)          |
|        help       | see this table                                         |
|     screenshot    | take a screenshot of bot and save to cwd of mothership |
|  shell*<command>  | execute a shell command on bot                         |
|  grab*<file_name> | transfer a file from cwd of bot to cwd of mothership   |
| upload*<filename> | transfer a file from cwd of mothership to cwd of bot   |
|     cd*<path>     | change cwd of bot                                      |
|     status        | get os memory and cpu statistics of remote client      |
|     cischeck      | get current cis complaint status of remote client      |
|     cisenable     | make remote system cis complaint                       |
|     message       | send message to the remote host                        |
|     splunkenable  | enable splunk forwarder on remote host                 |
|     users         |  get a list of users on the remote host                |
  
 

- The help command(for e.g.) outputs:

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/17.PNG">

- The showclients command outputs:

<img width="600" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/3.PNG">

- The status command is used to view the system-information of the connected clients:

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/4.PNG">


- The users command outputs:

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/5.PNG">

One can choose which user to view(system or normal):

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/6.PNG">

- Few more examples of other commands:

**cd**:

<img width="200" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/7.PNG">

**grab**:

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/8.PNG">

- The **cischeck** command checks for the current status of CIS Compliance and Benchmarks of the client:

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/10.PNG">

- The **cisenable** command enables all the disabled CIS Compliance and Benchmarks:

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/11.PNG">

- For more INformation on CIS Compliance and Benchmarks:
Follow the link: https://www.rapid7.com/solutions/compliance/cis-benchmarks/

- The **splunkenable** command installs and configures splunk to forward system logs to our splunk server:

- Starting Splunk Server(Listening):

>before administring the splunkenable command splunkserver and gui must be set up and listening on server side  

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/1.PNG">

- Running the **splunkenable** command and waiting for the splunk forwarder to get configured in the remote host:

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/12.PNG">

- Completion of splunk forwarder configuration in the remote host(client) and connection to server established(debian):

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/13.PNG">

- A user with knowledge of python can write his own functionalities that can be easily incorporated into the existing clients.

- User can quit the script safely using the exit command and the clients will go to sleep for 10 sec.After which they will go back to the task of trying to connect back to the MotherNode.So when the person starts the mothernode again his clients will connect back again:

<img width="500" alt="screen shot 2017-11-26 at 8 31 44 am" src="https://raw.githubusercontent.com/Vish-45/Centralised-Monitoring-And-Control-System/master/snaps/15.PNG">


# HOW TO INSTALL
----
## MOTHERNODE
- To install just open the terminal and type:
```sh 
git clone https://github.com/Vish-45/Centralised-Monitoring-And-Control-System.git
```

To launch the MotherNode go to the installed folder and type
```python
python3 server.py <ip address> <port>
```
THE IP ADDRESS MUST BE YOUR LOCAL IP IF YOU WANT TO USE IN LAN.
TO USE IN WAN USE YOUR GLOBAL IP WITH APPROPRIATE PORT FORWARDING ON THE ROUTER.
refer
https://www.wikihow.com/Set-Up-Port-Forwarding-on-a-Router


## CLIENT
>NOTE agent is by the name of client.py
- Open the client.py file using any text editor
- Edit the IP and port fields to the IP and port you used above
- Save the file.
- copy the complete client folder to the remote host you wish to administer
- run the client script as root.
```python
python3 client.py
```




# UPDATES
----
New updates and bug fixes rolling out soon.

