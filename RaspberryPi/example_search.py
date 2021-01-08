#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
import time
import RPi.GPIO as GPIO
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)	# 릴레이 연결 핀
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)



## Search for a finger
##

## Tries to initialize the sensor
while(1) :
	if (GPIO.input(23)==False):
		try:
			f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

			if ( f.verifyPassword() == False ):
				raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
			print('The fingerprint sensor could not be initialized!')
			print('Exception message: ' + str(e))
			continue

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to enroll new finger
		try:
			print('Waiting for finger...')

			## Wait that finger is read
			while ( f.readImage() == False ):
				pass

			## Converts read image to characteristics and stores it in charbuffer 1
			f.convertImage(0x01)

			## Checks if finger is already enrolled
			result = f.searchTemplate()
			positionNumber = result[0]

			if ( positionNumber >= 0 ):
				print('Template already exists at position #' + str(positionNumber))
				continue

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
			print('New template position #' + str(positionNumber))

		except Exception as e:
			print('Operation failed!')
			print('Exception message: ' + str(e))
			continue

	elif (GPIO.input(24)==False):
		try:
			f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

			if ( f.verifyPassword() == False ):
				raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
			print('The fingerprint sensor could not be initialized!')
			print('Exception message: ' + str(e))
			continue

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
				continue
			else:
				print('Found template at position #' + str(positionNumber))
				print('The accuracy score is: ' + str(accuracyScore))
				GPIO.output(18, True )
				time.sleep(0.5)
				GPIO.output(18, False)
				
				
				

			## OPTIONAL stuff
			##

			## Loads the found template to charbuffer 1
			f.loadTemplate(positionNumber, 0x01)

			## Downloads the characteristics of template loaded in charbuffer 1
			characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

			## Hashes characteristics of template
			print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

		except Exception as e:
			print('Operation failed!')
			print('Exception message: ' + str(e))
			continue
			
			
	elif(GPIO.input(25)==False):
		try:
			f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

			if ( f.verifyPassword() == False ):
				raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
			print('The fingerprint sensor could not be initialized!')
			print('Exception message: ' + str(e))
			continue
		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to delete the template of the finger
		try:
			while ( f.readImage() == False ):
				pass
			f.convertImage(0x01)
			result = f.searchTemplate()

			positionNumber = result[0]

			if ( f.deleteTemplate(positionNumber) == True ):
				print('Template deleted!')

		except Exception as e:
			print('Operation failed!')
			print('Exception message: ' + str(e))
			continue
