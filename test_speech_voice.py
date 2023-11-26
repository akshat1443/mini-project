

from gtts import gTTS
import os
import sqlite3
import sys
import pyfingerprint
import hashlib
from  pyfingerprint import PyFingerprint
import tempfile
import datetime


def image():
 try:
    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    print('Downloading image (this take a while)...')
    currentDT = datetime.datetime.now()
    imageDestination =  tempfile.gettempdir() + '/fingerprint'+str(currentDT)+'.bmp'
    f.downloadImage(imageDestination)
    print('The image was saved to "' + imageDestination + '".')

 except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)



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

## Tries to search the finger and calculate hash
try:
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Searchs template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match found!')
        image();
        os.system('mpg321 Message.mp3')
        os.system("mpg321 positionnumber000.mp3")
        exit(0)
    else:
        print('Found template at position #' + str(positionNumber))
        os.system('mpg321 Message.mp3')
        os.system('mpg321 positionNumber' + str(positionNumber)+ '.mp3')
        print('The accuracy score is: ' + str(accuracyScore))

   
    ## Loads the found template to charbuffer 1
    f.loadTemplate(positionNumber, 0x01)

    ## Downloads the characteristics of template loaded in charbuffer 1
    characterics = instr(f.downloadCharacteristics(0x01)).encode('utf-8')

    ## Hashes characteristics of template
    print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)   
    
