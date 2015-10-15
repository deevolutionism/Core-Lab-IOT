#	An encryption / decoder program for the Raspberry Pi that uses bluetooth, and the FTDI and RFDuino.

#	Written by Johnny Dunn and Gentry Demchak

import threading
from Queue import Queue
import os
import math
import time
import sys
import string, socket, select
import RPI.GPIO as GPIO
import serial
serdata=""
serQ=Queue(20) 
ser = serial.Serial('/dev/ttyAMA0', 57600) #read incoming serial data

sendingMessage = True
receivingMessage = False
firstTimeRunning = True    #Is the program being run for the first time?
changeMode = True       #When changeMode is true, the program goes back to sending / receiving options

randomKey       #Decoder key that is randomized every time program begins. Neither users will ever see the key, so it is more secure. 

main()

def startInterface ():
    if (firstTimeRunning == True):
        #Begin messaging
        print("Encrypted messaging system now running.\n")
        inputActivate = (raw_input('Sending or receiving message(s)? (Send / Receive) '))
            elif (inputActivate == 'Send'):
                sendingMessage = True
                receivingMessage = False
                randomKey = randrange(-9,9)
                print("\nRandomized, one-time key has been generated.")
                ser.write(randomKey)
                firstTimeRunning = False;
            else: 
                receivingMessage = True
                sendingMessage = False
                ser.read()
                randomKey = ser.read()
                print("Randomized, one-time key has been found and secured.")
    if (firstTimeRunning == False && changeMode == True):
	   inputActivate = (raw_input('Sending or receiving message(s)? (Send / Receive) '))
       changeMode = False
        elif (firstTimeRunning == False && inputActivate == 'Send'):
            sendingMessage = True
            receivingMessage = False
            print("\nNow sending encrypted messages. Enter 'sudo back' to change modes to receive encrypted messages.\n")
        else: 
    	   sendingMessage = False
    	   receivingMessage = True
    	   print("\nNow decoding received messages. Enter 'sudo back' to change modes to send encrypted messages.\n")
        elif (sendingMessage == True):
    	   sendMessage()
        else:
    	   receiveMessage()

def sendMessage ():
	sentMessage = input("Please enter the message to encode: ")
   # if (sentMessage == "sudo back"):        #User wishes to switch modes
    #    changeMode = True
     #   print("\nBack..")
      #  startInterface()                        #Interface begins again to switch modes
    print("\nMessage encoded: ")
    #Loop through the message and print out the coded numerical values
    for ch in range(0, len(sentMessage)):
        encryptedMessage = encryptedMessage + chr(ord)(sentMessage[ch]) + randomKey) #, end=" "
        print(encryptedMessage + "\n")
        ser.write(encryptedMessage)
        encryptedMessage = ""
    successfulMessage = input("Continue sending messages? (Yes / No): ")
    if (sucessfulMessage == "Yes" || "yes"):
        changeMode = False
        startInterface()
    elif sucessfulMessage == "No" || "no"):
        changeMode = True
        startInterface()
    else: 
        print("Command not understood!")
        changeMode = False
        startInterface()

def receiveMessage ():
    recievedMessage = ser.readline() #store incoming serial data in variable
    print ("\nReceived encrypted message: " + receivedMessage)
    #receivedMessage = input("Enter encrpyted message: ")
  #  if (receivedMessage == "sudo back"):            #User wishes to switch modes
   #     changeMode = True
    #    print("\nBack..")
     #   startInterface()                 #Interface begins again to switch modes
    #chars = []
    #Loop through the message and print out the decoded values
    for ch in receivedMessage.split():    #Messages are separated by spaces by default to distinguish words
        decodedMessage = decodedMessage + chr(ord(receivedMessage.split[ch] - randomKey))
        #codeMsg = eval(splitMsg)    #Converts digits to a number
        #chars.append(chr(ord()code))     #Accumulates characters
    #decodedMessage = "".join(chars)           #Message is formed from characters
    print("\nDecoded Message: ", decodedMessage)       #Prints out the decoded message
    seenMessage = input("Continue receiving messages? (Yes / No): ")
    if (seenMessage == "Yes" || "yes"):
        changeMode = False
        startInterface()
    elif seenMessage == "No" || "no"):
        changeMode = True
        startInterface()
    else: 
        print("Command not understood!")
        changeMode = False
        startInterface()

def main ():
	startInterface()