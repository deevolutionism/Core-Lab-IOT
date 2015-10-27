#	An encrypted messaging for the Raspberry Pi / computer (Depending on the serial driver) that uses FTDI and RFDuino.
#   The encryption code is randomized every time the program is run. Neither users know the encryption key for added security.
#	Written by Johnny Dunn and Gentry Demchak
#	Sender = host device

import threading
from threading import Thread
from queue import Queue
#from queue import 
import os
import math
import random
import time
import sys
import string, socket, select
#import RPI.GPIO as GPIO
import serial
import getpass 
serdata=""
serQ=Queue(20) 
ser = serial.Serial('COM6', 9600)   #Reads incoming serial data. Change the directory and
global sendingMessage                        #of this driver to switch between platforms (Pi and computer).
global receivingMessage
global firstTimeRunning   #Is the program being run for the first time?
global changeMode       #When changeMode is true, the program goes back to sending / receiving options
global randomKey       #Encryption / decoder key that is randomized every time program begins. Neither users will ever see the key, so it is more secure. 
global broadcastingKey     #Is the key being broadcast by the sender?
global keyPass             #String to be filtered out of the messages; for further device security
global inputActivate         #Text comamnd user sends to activate sending / receiving
global encryptedMessage      #Message that the sender inputs to be encrypted   
global receivedMessage
global successfulMessage       #Input asking if user wants to keep sending messages
global seenMessage             #Input asking if user wants to keep receiving messages
global decodedMessage
#String userMessage				#The message that the host sends to the receiver

firstTimeRunning = True
changeMode = False
broadcastingKey = False

def beginSetup ():
    global sendingMessage
    global receivingMessage
    global randomKey
    global firstTimeRunning
    global broadcastingKey    
    global sendingMessage
    global receivingMessage
    global randomKey
    global firstTimeRunning
    global broadcastingKey
    global inputActivate
    print("Encrypted messaging system now running.\n")
    keyPass = getpass.getpass(prompt='Enter pass key to find device: ')
    print("Pass key has been stored.")
    inputActivate = input('Sending or receiving message(s)? (Send / Receive) ')
    if (inputActivate == 'Send'):       #User is the sender
        sendingMessage = True
        receivingMessage = False
        randomKey = random.randrange(-9,9)     #Cipher key is generated that adds or subtracts randomized value to encryption
        firstTimeRunning = False        #Skip the introduction next time
        print("\nRandomized, one-time key has been generated.")
        broadcastingKey = True         #Turn on key broadcasting
        if (broadcastingKey == True):          
            print("Yeah")
            #ser.write(randomKey)        #Key is broadcasted through serial writing to RFDuino
			#Send randomKey key that was generated to user
    elif (inputActivate == 'Receive'):  #User is the receiver
            receivingMessage = True
            sendingMessage = False
            firstTimeRunning = False        #Skip the introduction next time
            if (broadcastingKey == True):   #Is the sender broadcasting a key?  
            #ser.read()                  #If so, read the key
            #randomKey = ser.read()      #Get the key as an object
                broadcastingKey = False     #Turn the key broadcasting off once key is gotten by receiver
                print("Randomized, one-time key has been found and secured.")
    else:
        print("Command not understood!")
        firstTimeRunning = True
        startInterface()

def startInterface ():                      #The terminal-based interface for the program. Also `
    global sendingMessage
    global receivingMessage
    global randomKey
    global firstTimeRunning
    global broadcastingKey
    global changeMode
    global inputActivate
    if (firstTimeRunning == True):          #First time running program?
        #Begin user setup
	    beginSetup()
    #Begins new message transmission
    if (firstTimeRunning == False & changeMode == True):       #Already started running program 
       inputActivate = input('Sending or receiving message(s)? (Send / Receive) ')
       changeMode = False
    elif (firstTimeRunning == False) & (inputActivate == 'Send'):
        sendingMessage = True
        receivingMessage = False
        print("\nNow sending encrypted messages. You can switch to receiving messages by typing 'back.'\n")
    elif (firstTimeRunning ==  False) & (inputActivate == 'Receive'): 
        sendingMessage = False
        receivingMessage = True
        print("\nNow decoding received messages. You can switch to sending messages by typing 'back.'\n")
    if (sendingMessage == True):
	    sendMessage()
	    receivingMessage = False
    elif (receivingMessage == True):
        receiveMessage()
        sendingMessage = False

def sendMessage ():
    global changeMode
    global encryptedMessage
    global successfulMessage
    global seenMessage
    global decodedMessage
    userMessage = input("Please enter the message to encode: ")			#Unencrypted message that the sender writes
    encryptedMessage = userMessage
    print("\nMessage encoded: ")
    ser.write(userMessage.encode())
    #Loop through the message and print out the coded numerical values
    #for ch in range(0, len(userMessage)):                   #For each character in the sent message
        #encryptedMessage = encryptedMessage + chr(ord)(userMessage[ch]) + randomKey #, end=" "  #Get the Unicode number value of the character and encode it
        #print(encryptedMessage + "\n")                                                           #further with the randomized key generated in the beginning 
        #ser.write(encryptedMessage)         #Sends the fully-encrypted message to RFDuino to communicate with other device
        #encryptedMessage = ""               #Resets encrypted message object
    successfulMessage = input("Continue sending messages? (Yes / No): ")   #After sending message, ask if user wants to keep sending
    if (successfulMessage == "Yes") & (successfulMessage == "yes"):
        changeMode = False
        startInterface() 
        #Message + chr(ord(receivedMessage.split[ch] - randomKey))   #Get the corresponding letter to Unicode number
        #codeMsg = eval(splitMsg)    #Converts digits to a number                           #and further decodes it with randomized key generated.
        #chars.append(chr(ord()code))     #Accumulates characters
    #decodedMessage = "".join(chars)           #Message is formed from characters
    print("\nDecoded Message: ", decodedMessage)       #Prints out the decoded message
    seenMessage = input("Continue receiving messages? (Yes / No): ")    #Asks if user wants to keep receiving messages or switch
    if (seenMessage == "Yes") & (seenMessage == "yes"):
        changeMode = False
        startInterface()                     #If yes, go back to main interface and skip setup screen
    elif (seenMessage == "No") & (seenMessage == "no"):
        changeMode = True
        startInterface()                     #If no, go back to main interface and set up sending / receiving
    else: 
        print("Command not understood!")
        changeMode = False
        startInterface()

def receiveMessage ():
    global changeMode
    global encryptedMessage
    global successfulMessage
    global seenMessage
    global decodedMessage
    global receivedMessage
    receivedMessage = 1231923
    decodedMessage = receivedMessage
    #receivedMessage = ser.readline() #Reads the incoming, wirelessly transmitted encrypted message from other device
    print ("\nReceived encrypted message: " + receivedMessage)
    #chars = []
    #Loop through the message and print out the decoded values
    for ch in receivedMessage.split():    #Messages are separated by spaces by default to distinguish words
        decodedMessage = decodedMessage + chr(ord(receivedMessage.split()[ch] - randomKey))   #Get the corresponding letter to Unicode number
        #codeMsg = eval(splitMsg)    #Converts digits to a number                           #and further decodes it with randomized key generated.
        #chars.append(chr(ord()code))     #Accumulates characters
    #decodedMessage = "".join(chars)           #Message is formed from characters
    print("\nDecoded Message: ", decodedMessage)       #Prints out the decoded message
    seenMessage = input("Continue receiving messages? (Yes / No): ")    #Asks if user wants to keep receiving messages or switch
    if (seenMessage == "Yes") & (seenMessage == "yes"):
        changeMode = False
        startInterface()                     #If yes, go back to main interface and skip setup screen
    elif (seenMessage == "No") & (seenMessage == "no"):
        changeMode = True
        startInterface()                     #If no, go back to main interface and set up sending / receiving
    else: 
        print("Command not understood!")
        changeMode = False
        startInterface()

def main ():
	startInterface()                         #Begins Terminal interface for encryption program
	
main()