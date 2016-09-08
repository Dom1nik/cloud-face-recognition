#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Dominik

DESCRIPTION:
	Function for detecting frontal faces on an input frame.
	Detection is done with the haar classifier library using pretrained face model .xml file (included in standard OpenCV build).

INPUT: 
	img = cv2.imread("/path/to/image/img")
"""

import cv2

def detect(img):
	
	cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
	
	# If no faces are detected, return empty list, else return face coordinates.
	if len(rects) == 0:
		return []
	
	return rects


