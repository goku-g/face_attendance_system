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




class atendance_window():
    
    def __init__(self, root, cap):
        self.root = root
        self.cap = cap
        
        self.interval = 10 # Interval in ms to get the latest frame
         
        
        # Create canvas for image
        self.image_frame = Canvas(self.root, width=image_width, height=image_height)
        self.image_frame.pack(side=LEFT)
                
        
        
        

        #START attendance section
        # self.main_frame = Canvas(self.root, width=total_width-image_width, height=total_height, bg="white")
        # self.main_frame.pack()
        
        # self.gap_txt = Label(self.main_frame ,text = "Recent Check In", fg="red").grid(row = 0,column = 1)
        #END attendance section

        # INFO section
        self.scroll_y = Scrollbar(self.root)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        self.info_frame = Text(self.root, width=total_width-image_width, height=int(total_height/2), yscrollcommand=self.scroll_y.set, bg="gray")
        self.info_frame.pack()

        self.scroll_y.config(command=self.info_frame.yview)
        # END info section

        # self.entry_info = Text(self.main_frame, width=total_width-image_width, height=int(total_height/2), bg="blue")
        # self.entry_info.grid(row=1,column=0)
        
        
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
                    
            
            face_names.append(name)
            face_ids.append(ID)
        
        i = 0
        for y,w,h,x in face_locations:
            i += 1

        if i == 1:
            
            if face_names[i-1] != "Not recognize":
                
                if face_ids[i-1] in att_ids:
                    
                    message = f"\n    ID : {face_ids[i-1]}  Already checked in."
                    self.info_frame.insert('1.0', message)
                    
                    
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

                    message = f"\n>>ID: {face_ids[i-1]} Name: {face_names[i-1]}, Attendence done."
                    self.info_frame.insert('1.0', message)

                    # show attendee details -start
                    
                    # self.id_value_txt = Label(self.main_frame ,text = "Id").grid(row = 1,column = 1)
                    # self.name_txt = Label(self.main_frame ,text = "Name").grid(row = 3,column = 0)
                    # self.gap_txt = Label(self.main_frame ,text = " ").grid(row = 3,column = 1)
                    # self.time_txt = Label(self.main_frame ,text = "Time").grid(row = 3,column = 2)

                    # self.id_value = Label(self.main_frame ,text = str(face_ids[i-1]), fg="blue").grid(row = 2,column = 1)
                    # self.name = Label(self.main_frame ,text = str(face_names[i-1]), fg="blue").grid(row = 4,column = 0)
                    # self.gap = Label(self.main_frame ,text = " ").grid(row = 4,column = 1)
                    # self.time = Label(self.main_frame ,text = str(datetime.datetime.now()), fg="blue").grid(row = 4,column = 2)
                    
                    # show attendee details -end

                    # self.root.destroy()
                    # main_for_entry()
                    
            else:
                message = "\n>>You are Not recognize for the system."
                self.info_frame.insert('1.0', message)
                
        

        elif i == 0:
            
            message = "\n>>No one in the frame !!!!"
            self.info_frame.insert('1.0', message)
            
            
            
        else:
            
            message = "\n>>More than 1 person in frame. So, Clear noise."
            self.info_frame.insert('1.0', message)


def main_for_attendee():
    
    global known_dir
    global ids
    global names
    global faces
    global times
    global total_width
    global total_height
    global image_data
    global image_width
    global image_height
    global att_ids
    global att_names
    global check_in
    global check_out

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

    # global img2save
    #image_data = []
    
    root = Tk()
    root.geometry(total_dim)
    root.title("Face Attendence System")
    root.iconbitmap(known_dir+'/logo-icon.ico')
    
    atendance_window(root, cv2.VideoCapture(1))
    root.mainloop()

if __name__ == "__main__":
        
    main_for_attendee()