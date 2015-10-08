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

main()

def startInterface ():
    if (firstTimeRunning == True):
        #Begin messaging
       print("Encrypted messaging system now running.\n")
       firstTimeRunning = False;
    if (changeMode == True):
	   inputActivate = (raw_input('Sending or receiving message(s)? (Send / Receive) '))
       changeMode = False
 	elif (inputActivate == 'Send'):
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
    if (sentMessage == "sudo back"):        #User wishes to switch modes
        changeMode = True
        print("\nBack..")
        startInterface()                        #Interface begins again to switch modes
    print("\nMessage encoded: ")
    #Loop through the message and print out the coded numerical values
    for ch in sentMessage:
        ord(ch), end=" ") = encodedMessage          
        print(encodedMessage)
        ser.write(encodedMessage)

def receiveMessage ():
    recieved = ser.readline() #store incoming serial data in variable
    print recieved
    receivedMessage = input("Enter encrpyted message: ")
    if (receivedMessage == "sudo back"):            #User wishes to switch modes
        changeMode = True
        print("\nBack..")
        startInterface()                 #Interface begins again to switch modes
    chars = []
    #Loop through the message and print out the decoded values
    for splitMsg in receivedMessage.split():    #Messages are separated by spaces by default to distinguish words
        codeMsg = eval(splitMsg)    #Converts digits to a number
        chars.append(chr(codeNum))     #Accumulates characters
    decodedMessage = "".join(chars)           #Message is formed from characters
    print("\nDecoded Message: ", decodedMessage)       #Prints out the decoded message

def main ():
	startInterface()