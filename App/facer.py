#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Dominik

DESCRIPTION:
	Script for livefeed (camera input frame) face detection via opencv_detect() function and face detection and recognition via FaceR Animetrics cloud API.
	Detect function is checking all thirtieth frame in the row. 
	
	If face is detected via OpenCV, detection needs to be done again, this time using FaceR cloud detect function 
	(this way FaceR image_id will be generated, which is, along with face coordinates,
	a key argument needed to start FaceR recognition. In case face is detected via Facer detect function, Facer recognition function is called,
	which is then returning confidence level (percent, %) 
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


def start_recognition():
	
	print "********** Facer Animetrics *******************************************************"
	cap = cv2.VideoCapture(0)
	frame_num = 0
	#bg_image = cv2.imread("icon/main_bg.png")	
	search_icon = cv2.imread("icon/waiting_2.jpg")
	access_icon = cv2.imread("icon/approvedfont.jpg")
	no_access_icon = cv2.imread("icon/notapprovedfont.jpg")
	error_icon = cv2.imread("icon/error.jpg")
	
	# Loop camera input frame reading, detection and recognition.
	while(1):
		frame_num += 1
		threshold = 70
		_, frame = cap.read()
		key = cv2.waitKey(5) & 0xFF
		cv2.imshow('Face Recognition System (livefeed)', frame) 
		# Check for faces (OpenCV detection) on every thirtieth frame.		
		if frame_num == 30:
			frame_num = 0
			rects = []
			rects=opencv_detect.detect(frame)
			# If face detected, start face detection via cloud API.
			if len(rects):
				print "Face detected!"
				cv2.imshow('Face Recognition System (livefeed)', search_icon)  
				key = cv2.waitKey(5) & 0xFF
				cv2.imwrite('frame.jpg', frame)	
					
				try:
					response = unirest.post("https://animetrics.p.mashape.com/detect?api_key=4adf13e6b744dee183476cc0574a7df6",
					  headers={
						"X-Mashape-Key": "Ugdk0HPDgLmshEOPogyrGTxr9B4Dp1h7TSxjsng80cdpz6amIi"
					  },
					  params={
						"image": open("frame.jpg", mode="rb"),
						"selector": "FULL"
					  }
					)
					result = response.body
					# If face detected via cloud API, start face recognition via cloud API.
					if result['images'][0]['faces']:
						
						image_id=result['images'][0]['image_id']
						width=result['images'][0]['faces'][0]['width']
						height=result['images'][0]['faces'][0]['height']
						topLeftX=result['images'][0]['faces'][0]['topLeftX']
						topLeftY=result['images'][0]['faces'][0]['topLeftY']
						
						try:
							print "Starting recognition of the detected face."
							response = unirest.get("https://animetrics.p.mashape.com/recognize?api_key=4adf13e6b744dee183476cc0574a7df6&gallery_id=GROUP_NAME&height={0}&image_id={1}&topLeftX={2}&topLeftY={3}&width={4}".format(height,image_id,topLeftX,topLeftY,width),
							  headers={
								"X-Mashape-Key": "Ugdk0HPDgLmshEOPogyrGTxr9B4Dp1h7TSxjsng80cdpz6amIi",
								"Accept": "application/json"
							  }
							)
							print ""				
							print "*****************"
							print response.body
							print "*****************"
							print ""				
							
							result_precision_rate = float(response.body['images'][0]['candidates']['PERSON_NAME'])
							result_precision_rate *= 100
							
							# If recognition is positive, than if confidence is >= to threshold, access is granted, match is confirmed, else access is not granted and match is not confirmed.
							if result_precision_rate >= threshold:
								print "Face recognized with confidence of {0:.2f}, access granted.".format(result_precision_rate)
								cv2.imshow('Face Recognition System (livefeed)', access_icon)
								key = cv2.waitKey(10) & 0xFF
							else:
								print "Face not recognized (confidence of {0:.2f}%), access not granted.".format(result_precision_rate)
								cv2.imshow('Face Recognition System (livefeed)', no_access_icon)
								key = cv2.waitKey(10) & 0xFF
				
							time.sleep(3)
							
						except:
							print "SSLError on appending face to subject."
							cv2.imshow('Face Recognition System (livefeed)', error_icon)
							key = cv2.waitKey(10) & 0xFF
							time.sleep(3)
							pass
					else:
						print 'Facer face detection: no face found!' 
			
				except:
					print "SSLError on receiving detect info."
					cv2.imshow('Face Recognition System (livefeed)', error_icon)
					key = cv2.waitKey(10) & 0xFF
					time.sleep(3)
					pass
			
		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			break
	
	cap.release()
	cv2.destroyAllWindows()

















