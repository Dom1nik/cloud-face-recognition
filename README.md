
********************
DESCRIPTION
********************

While all sorts od Cloud APIs are becoming more and more popular in replacing local-based alternatives, this project was intented to demonstrate Face Recogition via Cloud, with OpenCV's Haar Classificator running locally and is used for detecting faces.

Project implements two optional Cloud APIs - Face++ and FaceR.
Recognition is done comparing locally detected face (using OpenCV) with person model pre-trained by few hundred images (total 505 images were used in a process using Cloud APIs).
Result of a Face recognition is confidence level which tells us what are the odds that unknown, detected face really belongs to the pretrained person model. Threshold of 70% is set for recognition to be successful.


********************
PREREQS (4)
********************

	1.) Obtain your API credentials
		To use Face++ API, obtain keys and do initial setting, follow this link: http://www.faceplusplus.com/create-a-new-app/
		To use FaceR API, Mashape API provider is used. Therefore, obtaining keys and initial settings is done on through Mashape.
			Link: https://market.mashape.com/animetrics/animetrics-face-recognition

	2.) New face model needs to be created and trained within a group, using each API separate. 
	3.) After doing previous steps, edit facer.py and faceplusplus scripts by replacing:
		OBTAINED KEYS (For facer.py, edit "api_key" and "X-Mashape-Key" variables; For faceplusplus.py, edit "API_KEY" and "API_SECRET" variables),
		Person name and group name (search for and replace all "PERSON_NAME" with new trained model name, "GROUP_NAME" with new group name.

	4.) INSTALL
		OpenCV 2.4.10 or lower
		Python 2.7
		Unirest
		ImageTk 
	
********************
RUN PROGRAM
********************

	1.) Open terminal
	2.) Go to project directory (readme.txt location folder)
	3.) Type following command: python face_recognition_GUI.py


********************
NOTE
********************
	To use Face++ SDK for testing purposes, you need to edit API keys in apikey.cfg file.
	To start SDK, enter the following command in the project directory:
		"python cmdtool.py".
Contact GitHub API Training Shop Blog About
© 2016 GitHub, Inc. Terms Privacy Security Status Help
