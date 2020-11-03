import paramiko
import time
from getpass import getpass
import sys
import os
import json
import routeros_api
from datetime import datetime

try:
	ip_addr = input("Input IP Address: ")

	print (f"\nCheck Connection {ip_addr}")
	respon = os.system(f"ping {ip_addr}")
	if respon == 0:
		print (f"\n{ip_addr} Connected\n")
	else:
		print (f"\n{ip_addr} Not Connected\n")

	while True:
		try:
			input_file = input("Input Your Configuration File: ")
			read_file = open(input_file, "r").readlines()
			break
			
		except IOError:
			print("File Not Found!!")
			continue

	username = input("Username: ")
	password = getpass()

	ssh_login = paramiko.SSHClient()
	ssh_login.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_login.connect(hostname=ip_addr, username=username, password=password)

	print (f"\nSuccess Login to {ip_addr}")
	print ("\nIs Configuring.....")

	for config in read_file:
		ssh_login.exec_command(config)
		time.sleep(1)

	time = datetime.now()
	print (f"\nSuccessful Configuring {ip_addr}")
	print("At " + time.strftime("%Y") + "-" + time.strftime("%m") + "-" + time.strftime("%d")
		+ " " + time.strftime("%H") + ":" + time.strftime("%M") + ":" + time.strftime("%S"))
	ssh_login.close()

	connection = routeros_api.RouterOsApiPool(
		host='{}'.format(ip_addr),
		username='{}'.format(username),
		password='{}'.format(password),
		port=8728,
	    plaintext_login=True
	)
	api = connection.get_api()
	
	print(f"\nDevice Detail Of {ip_addr}")
	show = api.get_resource('/system/routerboard')
	get = show.get()
	for i in get:
		print(json.dumps(i, indent=4))
	connection.disconnect()

except KeyboardInterrupt:
   	print ("\n\nExit The Program...\n")
   	sys.exit()
