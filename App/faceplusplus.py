#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Dominik

DESCRIPTION:
	Script for livefeed (camera input frame) face detection via opencv_detect() function and face recognition via Face++ cloud API.
	Detect function is checking all thirtieth frame in the row. 
	If face is detected, face coordinates are sent to cloud API which is then returning confidence level (percent, %) 
	that unknown detected face belongs to a trained model (person).

		
NOTE:		
	API KEYS and model_name ('PERSON_NAME') and belonging group ('GROUP_NAME') need to be changed before usage.

"""

import glob
import unirest
import time
import os
import cv2
import opencv_detect
import ctypes 
from facepp import API, File

# Register App first, API key/secret needed
SERVER = 'http://api.us.faceplusplus.com/'
API_KEY = '4c764c549faf0186ba0377f829411227'
API_SECRET = 'P4E7XwSTt50RkX2JFyRuBRNIk2mPDkgW'

api = API(API_KEY, API_SECRET, SERVER)


def start_recognition():

	print "********** Face++ *****************************************************************"
	# Opening camera input port.
	cap = cv2.VideoCapture(0)
	frame_num = 0
	threshold = 70
	# Pre-loading decoration images.
	search_icon = cv2.imread("icon/waiting_2.jpg")
	access_icon = cv2.imread("icon/approvedfont.jpg")
	no_access_icon = cv2.imread("icon/notapprovedfont.jpg")
	error_icon = cv2.imread("icon/error.jpg")

	
	# Loop camera input frame reading, detection and recognition.
	while(1):
		frame_num += 1
		_, frame = cap.read()
		key = cv2.waitKey(5) & 0xFF
		cv2.imshow('Face Recognition System (livefeed)', frame)  		
		# Check for faces (OpenCV detection) on every thirtieth frame.
		if frame_num == 30:
			frame_num = 0
			rects = []
			rects=opencv_detect.detect(frame)
			# If face detected, start face recognition via cloud API.
			if len(rects):
				cv2.imshow('Face Recognition System (livefeed)', search_icon)  
				key = cv2.waitKey(5) & 0xFF
				print "Face detected!"
				cv2.imwrite('frame.jpg', frame)	
				print "Starting recognition of the detected face."
				# Face++ cloud API call. Detected face is compared to pretrained group of person faces, and person with the highest confidence is returned, if any.
				try:
					response = api.recognition.identify(group_name='GROUP_NAME', img=File(r'frame.jpg'), mode='oneface')
					
					print ""				
					print "*****************"
					print response
					print "*****************"
					print ""	
					
					# If recognition is positive, than if confidence is >= to threshold, access is granted, match is confirmed, else access is not granted and match is not confirmed.
					if response['face']:
						result_precision_rate = float(response['face'][0]['candidate'][0]['confidence'])
						if result_precision_rate >= threshold:
							print "Face recognized with confidence of {0:.2f}%, access granted.".format(result_precision_rate)
							cv2.imshow('Face Recognition System (livefeed)', access_icon)
							key = cv2.waitKey(10) & 0xFF
						else:
							print "Face not recognized (confidence of {0:.2f}%), access not granted.".format(result_precision_rate)
							cv2.imshow('Face Recognition System (livefeed)', no_access_icon)
							key = cv2.waitKey(10) & 0xFF
		
						time.sleep(3)
					else:
						print "Face not recognized, access not granted!"
						cv2.imshow('Face Recognition System (livefeed)', no_access_icon)
						key = cv2.waitKey(10) & 0xFF
				except:
					print "OpenCV face parameters not recognized."
					cv2.imshow('Face Recognition System (livefeed)', error_icon)
					key = cv2.waitKey(10) & 0xFF
					time.sleep(3)
					pass
		
		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			break
	
	cap.release()
	cv2.destroyAllWindows()

















