from tkinter import *
from PIL import ImageTk,Image
# import tkMessageBox
import datetime


#import for image
import face_recognition
import cv2
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt




class atendence_window():
    
    def __init__(self, root, cap):
        self.root = root
        self.cap = cap
        
        self.interval = 20 # Interval in ms to get the latest frame
         
        
        # Create canvas for image
        self.image_frame = Canvas(self.root, width=image_width, height=image_height)
        self.image_frame.pack(side=LEFT)
        
        
        #START Entry section
        self.main_frame = Canvas(self.root, width=total_width-image_width, height=int(image_height/2), relief=FLAT)
        self.main_frame.pack(side =TOP)
        
        self.gap_txt = Label(self.main_frame ,text = "Recent Check In", fg="red").grid(row = 0,column = 1)
        
        '''
        self.id_value_txt = Label(self.main_frame ,text = "Id").grid(row = 1,column = 1)
        self.first_name_txt = Label(self.main_frame ,text = "First Name").grid(row = 3,column = 0)
        self.middle_name_txt = Label(self.main_frame ,text = "Middle Name").grid(row = 3,column = 1)
        self.last_name_txt = Label(self.main_frame ,text = "Last Name").grid(row = 3,column = 2)

        
        self.id_value = Entry(self.main_frame, relief=GROOVE )
        self.id_value.grid(row = 2,column = 1)
        self.first_name = Entry(self.main_frame, relief=GROOVE )
        self.first_name.grid(row = 4,column = 0)
        self.middle_name = Entry(self.main_frame, relief=GROOVE )
        self.middle_name.grid(row = 4,column = 1)
        self.last_name = Entry(self.main_frame, relief=GROOVE )
        self.last_name.grid(row = 4,column = 2)
        
        

        self.gap = Label(self.main_frame ,text = " ").grid(row = 5,column = 1)

        self.capture_button = Button(self.main_frame, text ="Take Picture", command = self.capture_photo, bg="#4293f5", fg = "#ffffff" ).grid(row=6,column=1)

        self.gap = Label(self.main_frame ,text = " ").grid(row = 7,column = 1)
        self.gap = Label(self.main_frame ,text = " ").grid(row = 8,column = 1)

        self.submit_button = Button(self.main_frame, text ="Submit", command = self.submit_details, bg="#58ed78" ).grid(row=9, column=0)
        self.quit_button = Button(self.main_frame, text ="Quit", command = self.quit_all, bg ="#c90a0a", fg = "#ffffff").grid(row=9, column=2)

        #END Entry section
        '''
        
        # INFO section
        self.info_frame = Canvas(self.root, width=total_width-image_width, height=int(image_height/2), relief=FLAT)
        self.info_frame.pack()
        
        # Update image on canvas
        self.update_image()
    
        
    def update_image(self):
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.image = cv2.flip(self.image, 1)
        
        # self.image = cv2.rectangle(self.image, (3,3), (image_width-2,image_height-6), (255, 0, 0), 2)
        self.image = self.image[ 3:image_height-6, 3:image_width-2]
        # self.image = cv2.resize(self.image, (image_width, image_height), interpolation = cv2.INTER_AREA)
        
        # recognize who wants to give attendence:
        self.save_data(self.image)
        
        self.image = Image.fromarray(self.image) # to PIL format
        self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
        # Update image
        
        self.image_frame.create_image(0, 0, anchor=NW, image=self.image)
        # Repeat every 'interval' ms
        self.root.after(self.interval, self.update_image)
    
        # check their are only one many people:
    def save_data(self, image):
        
        global no_one_frame
        global more_than_one_frame
        global success_msg
        
        new_img = image
        
        face_locations = face_recognition.face_locations(new_img)

        face_encodings = face_recognition.face_encodings(new_img, face_locations)

        face_names = []
        face_ids = []
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(faces, face_encoding)
            name = "Not recognize"
            ID = "NULL"

            face_distances = face_recognition.face_distance(faces, face_encoding)
            
            
                
            if face_distances.size > 0: # check whether the face_distances is empty or not
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = names[best_match_index]
                    ID = ids[best_match_index]
                    
            else:
                print(" ")
            
            face_names.append(name)
            face_ids.append(ID)
        
        i = 0
        for y,w,h,x in face_locations:
            i += 1

        if i == 1:
            
            if face_names[i-1] != "Not recognize":
                
                if face_ids[i-1] in att_ids:
                    
                    if success_msg:
                        message = "You are already checked in."
                        self.message = Label(self.info_frame ,text = message, fg="blue", font=("Helvetica", 12))
                        self.message.pack()
                        
                        no_one_frame = True
                        more_than_one_frame = True
                        success_msg = False
                    
                else:
                    att_ids.append(face_ids[i-1])
                    att_names.append(face_names[i-1])
                    check_in.append(datetime.datetime.now())

                    # delete old data.
                    file = open(os.path.join( known_dir, "attendence_report.pickle"), 'w')
                    file.close()

                    # dump new data
                    with open(os.path.join( known_dir, "attendence_report.pickle"), 'wb') as file:
                        pickle.dump([att_ids, att_names, check_in], file)

                    # if success_msg:
                        # message = f"ID: {face_ids[i-1]} Name: {face_names[i-1]}, Attendence done."
                        # self.message = Label(self.info_frame ,text = message, fg="green", font=("Helvetica", 12))
                        # self.message.pack()

                        # no_one_frame = True
                        # more_than_one_frame = True
                        # success_msg = False

                    # show attendee details -start
                    
                    self.id_value_txt = Label(self.main_frame ,text = "Id").grid(row = 1,column = 1)
                    self.name_txt = Label(self.main_frame ,text = "Name").grid(row = 3,column = 0)
                    self.gap_txt = Label(self.main_frame ,text = " ").grid(row = 3,column = 1)
                    self.time_txt = Label(self.main_frame ,text = "Time").grid(row = 3,column = 2)

                    self.id_value = Label(self.main_frame ,text = str(face_ids[i-1]), fg="blue").grid(row = 2,column = 1)
                    self.name = Label(self.main_frame ,text = str(face_names[i-1]), fg="blue").grid(row = 4,column = 0)
                    self.gap = Label(self.main_frame ,text = " ").grid(row = 4,column = 1)
                    self.time = Label(self.main_frame ,text = str(datetime.datetime.now()), fg="blue").grid(row = 4,column = 2)
                    
                    # show attendee details -end

                    # self.root.destroy()
                    # main_for_entry()
                    
            # else:
                # message = "You are Not recognize for the system."
                # self.message = Label(self.info_frame ,text = message, fg="red", font=("Helvetica", 12))
                # self.message.pack()
                
        

        elif i == 0:
            if no_one_frame:
                message = "No one in the frame !!!!"
                self.message = Label(self.info_frame , text = message, fg="red", font=("Helvetica", 12))
                self.message.pack()
                
                more_than_one_frame = True
                success_msg = True
                no_one_frame = False
            
            elif no_one_frame == False and more_than_one_frame == False:
                message = "No one in the frame !!!!"
                self.message = Label(self.info_frame , text = message, fg="red", font=("Helvetica", 12))
                self.message.pack()
                
                more_than_one_frame = True
            
            
        else:
            if more_than_one_frame:
                message = "More than 1 person (or no one) in frame. So, Clear noise."
                self.message = Label(self.info_frame , text = message, fg="red", font=("Helvetica", 12))
                self.message.pack()
                
                no_one_frame = True
                success_msg = True
                more_than_one_frame = False
                
            elif no_one_frame == False and more_than_one_frame == False:
                message = "More than 1 person (or no one) in frame. So, Clear noise."
                self.message = Label(self.info_frame , text = message, fg="red", font=("Helvetica", 12))
                self.message.pack()
                
                no_one_frame = True


def main_for_attendee():
    
    # global img2save
    #image_data = []
    
    root = Tk()
    root.geometry(total_dim)
    root.title("Face Attendence System")
    
    atendence_window(root, cv2.VideoCapture(1))
    root.mainloop()

if __name__ == "__main__":
    
    total_width = 880
    total_height = 644
    total_dim = str(total_width) +"x"+ str(total_height)
    image_width = 480
    image_height = 644
    
    no_one_frame = True
    more_than_one_frame = True
    success_msg = True
    
    known_dir = "C:/Users/Goku/Documents/jupyter_data/known_image"
    
    
    #load face data from pickle
    try:
        with open(os.path.join( known_dir, "attendence_report.pickle"), 'rb') as file:
            att_ids, att_names, check_in = pickle.load(file)
            
    except:
        att_ids = []
        att_names = []
        check_in = []
        #print("reading error")
        
    try:
        with open(os.path.join( known_dir, "faceData.pickle"), 'rb') as file:
            ids, names, faces, times = pickle.load(file)
            
    except:
        ids = []
        names = []
        faces = []
        times = []
        #print("reading error")
    
    main_for_attendee()