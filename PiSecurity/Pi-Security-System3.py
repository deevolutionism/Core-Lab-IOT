#Raspberry Pi Seucrity System
#By: Gentry Demchak & Johnny Dunn
#A program with a visual interface that allows you to set a raspberry pi running as a 
#standalone security system. When the PIR motion sensor is set off, an alarm can be played,
#an email will be sent remotely to the user, and photo recordings will be taken using the pi camera. 
#These photos will also be sent to the user by email, and then purged from the pi's SD card. 

import datetime
import time

import RPi.GPIO as io
import picamera

import feedparser		# imports feedparser to parse XML feed
import subprocess
import smtplib
import socket
import time
from email.mime.text import MIMEText
import datetime
import urllib2

# startTime
# currentTime 
# elapsedTime

user='human@email.com'		# replace dtclass15@gmail.com with your personal gmail user or email, or youruser@newschool.edu for your school account
passwd='**************'		# replace *** with your password for the above account

summaryAuthor = ""
summaryTitle = ""

io.setmode(io.BCM)
camera = picamera.PiCamera()

currentTime = datetime.date.today().strftime("%B %d, %Y");

pir_pin = 17
io.setup(pir_pin, io.IN)         # activate input 
#pir debounce
pirState = False
lastPirState = False
lastDebounceTime = 0
debounceDelay = 5000

#remoteEmailSwitch = false
#buttonSwitch = false

motionDetected = True

# def millis():
# 	elapsedTime = time.time() - startTime
# 	return pastTime

# while True:
# 	# pir_pin = io.input(pir_pin)
# 	print(pir_pin)


def activateCamera(state):
	if state == True:
		if io.input(pir_pin):
			print("PIR ALARM")
			motionDetected == True;
	        camera.start_preview()
	        camera.capture('Photo taken at' + currentTime + 'PI-Secure.jpg')
	        time.sleep(0.5)
	
def debounce():
	reading = io.input(pir_pin)
	if reading != lastPirState:
		currentTime = time.clock()
		lastDebounceTime = currentTime
	
	if time.clock() - lastDebounceTime > debounceDelay:
		if reading != pirState:
			pirState = reading
			if pirState == True:
				pirState = False

	#take picture or not take picture
	activateCamera(pirState)

	#save the reading. Next time through the loop it'll be the lastPirState
	lastPirState = reading

while True:
	debounce()

#if (buttonSwitch == on || remoteEmailSwitch == on)

# def searchEmail(summary, title): 
# 	newmails = feedparser.parse("https://" + user + ":" + passwd + "@mail.google.com/gmail/feed/atom").entries
#     for i in newmails:		#for loop itterates through newmails feed
#         #print str(i.title)		# uncomment to print out each title of unread emails
#         #print str(i.author)
#        # if str(i.title)=="balls":	# replace the word Search with the title of the email you are searching for
#     	    #print "Email: Title"
#             #print str(i.summary)
# 	    summaryTitle = str(i.summary)
#            # if str(i.author)=="Gentry Demchak (demcg318@newschool.edu)": #replace this string with the author and email you are searching for 
# 	       # print "Email: Summary"
# 	        print str(i.summary)
# 	        summaryAuthor = str(i.author)
# 		summaryTitle = str(i.summary)
# 	        sendEmail(summaryAuthor, summaryTitle) #calls sendEmail function and passes author and summary into the message of the email document
#     time.sleep(60) #run every 60 seconds unless program is terminated


# def sendEmail(str1, str2):
#     # Change to your own account information
#     to = 'dunnj368@newschool.edu'
#     gmail_user = 'dunnj368@newschool.edu'
#     gmail_password = '@Newpassword9'
#     smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
#     smtpserver.ehlo()
#     smtpserver.starttls()
#     smtpserver.ehlo
#     smtpserver.login(gmail_user, gmail_password)
#     today = datetime.date.today()
#     # Very Linux Specific
#     arg='ip route list'
#     p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
#     data = p.communicate()
#     split_data = data[0].split()
#     ipaddr = split_data[split_data.index('src')+1]
#     extipaddr = urllib2.urlopen("http://icanhazip.com").read()
#     my_ip = 'Local address: %s\nExternal address: %s' %  (ipaddr, extipaddr)
#     msg = MIMEText(my_ip)
#     # fills subject of email with the strings which were taken from feedparser
#     msg['Subject'] =  'You recieved an email from ' +  str1 + ' ' + 'stating ' + str2 
#     msg['From'] = gmail_user
#     msg['To'] = to
#     time.sleep(5)
#     smtpserver.sendmail(gmail_user, [to], msg.as_string())
#     smtpserver.quit()