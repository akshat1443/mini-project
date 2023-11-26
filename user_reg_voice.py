
from flask import Flask, session, redirect, url_for, escape, request, render_template, flash
import sqlite3
import sys
import pyfingerprint
import time
import hashlib
from  pyfingerprint import PyFingerprint
import time
from gtts import gTTS
import os
import subprocess

def new_user():
   
    
    print('ENTER THE NEW USER:')
     
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Checks if finger is already enrolled
    result = f.searchTemplate()
    positionNumber = result[0]
    
    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        exit(0)

    print('Remove finger...')
    time.sleep(2)

    print('Waiting for same finger again...')

    ## Wait that finger is read again
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 2
    f.convertImage(0x02)

    ## Compares the charbuffers
    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')

    ## Creates a template
    f.createTemplate()

    ## Saves template at new position number
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print('ENTER THE NAME:' + str(positionNumber))
    r=raw_input()
    tts = gTTS(text=str(r) + 'is waiting outside please open the door', lang='en') 
    tts.save('positionNumber' + str(positionNumber) + '.mp3')
    print('New template position #' + str(positionNumber))
    
 

     
    


    
## Enrolls new finger
##

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to enroll new finger
try:
    print('Enter the admin password')
    r=input() 
 
    
    print('Enter the admin finger print')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Checks if finger is already enrolled
    result = f.searchTemplate()
    admin = result[0]
         
    if ( admin >=0 and admin<=7 and r==1234):
        print('access ok')
        time.sleep(3)
        new_user();
        
        
except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
   
