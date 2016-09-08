#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Dominik

DESCRIPTION:
	Main script (face-recognition livefeed recognition) for generating program GUI.
	GUI consists of two radiobuttons intented for choosing cloud API (Face++ or Facer Animetrics) and buttons 'Start Recognition', 'About' and 'Quit'.
	User can stop livefeed by typing 'q' letter or quit program at anytime by pressing the 'Quit' button.
"""

from Tkinter import Tk, BOTH, IntVar
from ttk import Frame, Button, Radiobutton, Style
from PIL import Image, ImageTk
import tkMessageBox
import Tkinter
import facer
import faceplusplus
import cv2

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.centerWindow()
        self.initUI()
        
    
    def centerWindow(self):
      
        w = 400
        h = 200

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        
    def initUI(self):
        
        photo = ImageTk.PhotoImage(file='icon/main_bg_4.jpg')
        w = Tkinter.Label(self,image=photo)
        w.photo = photo 
        w.place(x=0, y=0, relwidth=1, relheight=1)
        #ackground_label.pack()
        
        
        self.api = IntVar()
        self.parent.title("Face Recognition System")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)
        
        faceplus = Radiobutton(self, text="Face++", variable=self.api, value=1)
        faceplus.place(x=50, y=40)
        
        facer = Radiobutton(self, text="FaceR Animetrics", variable=self.api, value=2)
        facer.place(x=200, y=40)

        start = Button(self, text="Start Recognition",
            command=self.startRecognition)
        start.place(x=100, y=80)
        
        helpButton = Button(self, text="Help",
            command=self.giveHelp)
        helpButton.place(x=100, y=110)
    
        quitButton = Button(self, text="Quit",
            command=self.quitGUI)
        quitButton.place(x=100, y=140)
    
    
    def startRecognition(self):
        
		if self.api.get() == 1:
            faceplusplus.start_recognition()
        if self.api.get() == 2:
            facer.start_recognition()
        
    
    def giveHelp(self):
        
		lines = ['1.) Choose one API', '2.) Click on "Start Recognition"', '3.) Type "q" or press "Quit" to exit program.']
        tkMessageBox.showinfo('Instructions', "\n".join(lines))
        
        
    def quitGUI(self):
        
		self.destroy()
        exit()
        
    

def main():
    
	root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
