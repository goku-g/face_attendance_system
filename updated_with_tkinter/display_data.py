# This is for display all data in list format!!!

from tkinter import *
from PIL import ImageTk,Image
import datetime


#import for image
import face_recognition
import cv2
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

known_dir = "C:/Users/Goku/Documents/jupyter_data/known_image"


class ListWindow():
    
    def __init__(self, root):
        self.root = root
        
        # self.interval = 20 # Interval in ms to get the latest frame
        
        
        #START Entry section
        self.main_frame = Canvas(self.root, width=total_width-image_width, height=int(image_height/2), relief=FLAT)
        self.main_frame.pack()

        self.gap = Label(self.main_frame ,text = " ").grid(row = 0,column = 1)
        #self.gap = Label(self.main_frame ,text = " ").grid(row = 1,column = 1)
        
        self.id_value_txt = Label(self.main_frame ,text = "SN").grid(row = 2,column = 0)
        self.id_value_txt = Label(self.main_frame ,text = "ID").grid(row = 2,column = 1)
        self.first_name_txt = Label(self.main_frame ,text = "First Name").grid(row = 2,column = 2)
        self.middle_name_txt = Label(self.main_frame ,text = " ").grid(row = 2,column = 3)
        self.middle_name_txt = Label(self.main_frame ,text = "Middle Name").grid(row = 2,column = 4)
        self.middle_name_txt = Label(self.main_frame ,text = " ").grid(row = 2,column = 5)
        self.last_name_txt = Label(self.main_frame ,text = "Last Name").grid(row = 2,column = 6)
        self.last_name_txt = Label(self.main_frame ,text = " ").grid(row = 2,column = 7)
        self.date_txt = Label(self.main_frame ,text = "Date of Entry").grid(row = 2,column = 8)
        
        self.gap = Label(self.main_frame ,text = " ").grid(row = 3,column = 1)
        
        i = 0
        for ID,name,time in zip(ids, names, times):
            self.id_value_txt = Label(self.main_frame ,text = i+1).grid(row = 4+i,column = 0)
            self.id_value_txt = Label(self.main_frame ,text = ID).grid(row = 4+i,column = 1)
            self.first_name_txt = Label(self.main_frame ,text = name.split(' ')[0]).grid(row = 4+i,column = 2)
            self.middle_name_txt = Label(self.main_frame ,text = " ").grid(row = 4+i,column = 3)
            self.middle_name_txt = Label(self.main_frame ,text = name.split(' ')[1]).grid(row = 4+i,column = 4)
            self.middle_name_txt = Label(self.main_frame ,text = " ").grid(row = 4+i,column = 5)
            self.last_name_txt = Label(self.main_frame ,text = name.split(' ')[2]).grid(row = 4+i,column = 6)
            self.last_name_txt = Label(self.main_frame ,text = " ").grid(row = 4+i,column = 7)
            self.date_txt = Label(self.main_frame ,text = time).grid(row = 4+i,column = 8)
            i += 1
        
        self.gap = Label(self.main_frame ,text = " ").grid(row = 5+i,column = 1)
        
        self.enter_button = Button(self.main_frame, text ="Register", command = self.quit_all, bg="#4293f5", fg = "#ffffff" ).grid(row=6+i,column=1)
        self.enter_button = Button(self.main_frame, text ="Delete Data", command = self.quit_all, bg="red", fg = "#ffffff" ).grid(row=6+i,column=8)
        
        #END Entry section
            
        
    def quit_all(self):
        self.root.destroy()


def main_for_list():
    total_width = 880
    total_height = 644
    total_dim = str(total_width) +"x"+ str(total_height)
    image_width = 480
    image_height = 644

    #load face data from pickle
    try:
        with open(os.path.join( known_dir, "faceData.pickle"), 'rb') as file:
            ids, names, faces, times = pickle.load(file)

    except:
        ids = []
        names = []
        faces = []
        times = []
        print("reading error")

    # global img2save
    image_data = []

    root = Tk()
    root.geometry(total_dim)
    root.title("Face Attendence System")

    ListWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main_for_list()
