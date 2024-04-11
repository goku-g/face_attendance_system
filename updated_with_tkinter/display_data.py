# test for scrollable all data displaying windows

# This is for display all data in list format!!!

from tkinter import *
from tkinter import ttk
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
        self.main_frame = Canvas(self.root, relief=FLAT, height=total_height-20)
        self.main_frame.pack()

        # vertical scrollbar for see all data
        self.scroll_y = Scrollbar(self.main_frame)
        self.scroll_y.pack(pady=10, side=RIGHT, fill=Y)

        # horizontal scrollbar for see all data
        self.scroll_x = Scrollbar(self.main_frame,orient=HORIZONTAL)
        self.scroll_x.pack(side=BOTTOM, fill=X)

        # create the tree structure to show presented data
        self.display_data_tree = ttk.Treeview(self.main_frame, yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        


        # configure the scrollbar which scroll listed data
        self.scroll_y.config(command=self.display_data_tree.yview)
        self.scroll_x.config(command=self.display_data_tree.xview)

        # SETup default columns in tree frame
        self.display_data_tree['columns'] = ("sn","id","first_name","middle_name","last_name","date_of_entry")

        column_width = int((total_width)/6)
        min_width = int((total_width)/6)

        self.display_data_tree.column("#0", width=0, stretch=NO)
        self.display_data_tree.column("sn", anchor=CENTER, width=column_width, minwidth=min_width)
        self.display_data_tree.column("id", anchor=CENTER, width=column_width, minwidth=min_width)
        self.display_data_tree.column("first_name", anchor=W, width=column_width, minwidth=min_width)
        self.display_data_tree.column("middle_name", anchor=W, width=column_width, minwidth=min_width)
        self.display_data_tree.column("last_name", anchor=W, width=column_width, minwidth=min_width)
        self.display_data_tree.column("date_of_entry", anchor=W, width=column_width, minwidth=min_width)

        self.display_data_tree.heading("#0", text="", anchor=W)
        self.display_data_tree.heading("sn", text="SN", anchor=CENTER)
        self.display_data_tree.heading("id", text="ID", anchor=CENTER)
        self.display_data_tree.heading("first_name", text="First Name", anchor=W)
        self.display_data_tree.heading("middle_name", text="Middle Name", anchor=W)
        self.display_data_tree.heading("last_name", text="Last Name", anchor=W)
        self.display_data_tree.heading("date_of_entry", text="Entry Date", anchor=W)
        

        i = 0
        for ID,name,time in zip(ids, names, times):

            if i % 2 == 0:
                self.display_data_tree.insert( parent='', index='end', iid=i, text='', values = (i+1, ID, name.split(' ')[0], name.split(' ')[1], name.split(' ')[2], str(time).split('.')[0]))

            else:
                self.display_data_tree.insert( parent='', index='end', iid=i, text='', values = (i+1, ID, name.split(' ')[0], name.split(' ')[1], name.split(' ')[2], str(time).split('.')[0]))
            

            i += 1
            
        self.display_data_tree.pack(pady=10, padx=10)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(side=TOP)

        self.enter_button = Button(self.button_frame, text ="Delete Data", command = self.quit_all, bg="red", fg = "#ffffff" ).pack(side=RIGHT,padx=5, pady=5)
        self.enter_button = Button(self.button_frame, text ="Register", command = self.quit_all, bg="#4293f5", fg = "#ffffff" ).pack(pady=5)
        
        #END Entry section
            
        
    def quit_all(self):
        self.root.destroy()


def main_for_list():

    global known_dir
    global ids
    global names
    global faces
    global times
    global total_width
    global total_height
    global image_data


    total_width = 720
    total_height = 320
    total_dim = str(total_width) +"x"+ str(total_height)
    

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
    root.iconbitmap(known_dir+'/logo-icon.ico')

    ListWindow(root)
    root.mainloop()


if __name__ == "__main__":

    main_for_list()
    