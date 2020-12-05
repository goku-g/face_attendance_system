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

known_dir = "C:/Users/Goku/Documents/jupyter_data/known_image"


class EntryWindow():
    
    def __init__(self, root, cap):
        self.root = root
        self.cap = cap
        
        self.interval = 20 # Interval in ms to get the latest frame
         
        
        # Create canvas for image
        self.image_frame = Canvas(self.root, width=image_width, height=image_height)
        self.image_frame.pack(side=LEFT)
        
        
        #START Entry section
        self.main_frame = Canvas(self.root, width=total_width-image_width, height=int(image_height/2), relief=FLAT)
        self.main_frame.pack()


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
        
        type(self.id_value)

        self.gap = Label(self.main_frame ,text = " ").grid(row = 5,column = 1)

        self.capture_button = Button(self.main_frame, text ="Take Picture", command = self.capture_photo, bg="#4293f5", fg = "#ffffff" ).grid(row=6,column=1)

        self.gap = Label(self.main_frame ,text = " ").grid(row = 7,column = 1)
        self.gap = Label(self.main_frame ,text = " ").grid(row = 8,column = 1)

        self.submit_button = Button(self.main_frame, text ="Submit", command = self.submit_details, bg="#58ed78" ).grid(row=9, column=0)
        self.quit_button = Button(self.main_frame, text ="Quit", command = self.quit_all, bg ="#c90a0a", fg = "#ffffff").grid(row=9, column=2)

        #END Entry section
        
        # INFO section
        self.info_frame = Canvas(self.root, width=total_width-image_width, height=int(image_height/2), relief=FLAT)
        self.info_frame.pack()
        
        # Update image on canvas
        self.update_image()
        
    def capture_photo(self):
        #global img2save
        #print("click")
        cv2.destroyAllWindows()
        self.img2save = self.return_current_img()
        #plt.imshow(self.img2save)
        if not image_data:
            image_data.append(self.img2save)
        else:
            image_data.remove(image_data[0])
            image_data.append(self.img2save)
        
        
    def submit_details(self):
        #print("submit")
        cv2.destroyAllWindows()
        
            
        ID = self.id_value.get()
        Fname = self.first_name.get()
        Mname = self.middle_name.get()
        Lname = self.last_name.get()
        entry_date = datetime.datetime.now()


        if Fname and Lname and ID:

            self.id_value.delete(0, END)
            self.first_name.delete(0, END)
            self.middle_name.delete(0, END)
            self.last_name.delete(0, END)

            #print(f"ID : {ID}")
            #print(f"NAME : {Fname} {Mname} {Lname}")
            #print(f"Date : {entry_date}")
            #plt.imshow(image_data[0])
            
            
            if len(image_data) > 0:
                self.save_data(ID, Fname, Mname, Lname, entry_date)
                
            else:
                self.message = Label(self.info_frame ,text = "Image is not Captured yet.", fg="red", font=("Helvetica", 12))
                self.message.pack()
                
            

        else:
            self.message = Label(self.info_frame ,text = "Enter The Required Field [ ID, first name, last name ]", fg="red", font=("Helvetica", 12))
            self.message.pack()
        
            
        
    def quit_all(self):
        #print("quit")
        #cv2.destroyAllWindows()
        self.root.destroy()
        
    def update_image(self):
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.image = cv2.flip(self.image, 1)
        
#         self.image = cv2.rectangle(self.image, (3,3), (image_width-2,image_height-6), (255, 0, 0), 2)
        self.image = self.image[ 3:image_height-6, 3:image_width-2]
#         self.image = cv2.resize(self.image, (image_width, image_height), interpolation = cv2.INTER_AREA)
        
        
        
        self.image = Image.fromarray(self.image) # to PIL format
        self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
        # Update image
        
        self.image_frame.create_image(0, 0, anchor=NW, image=self.image)
        # Repeat every 'interval' ms
        self.root.after(self.interval, self.update_image)
        
    def return_current_img(self):
        # Get the latest frame and convert image format
#         self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image = self.cap.read()[1]
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.image = cv2.flip(self.image, 1)
        
        #         self.image = cv2.rectangle(self.image, (3,3), (image_width-2,image_height-6), (255, 0, 0), 2)
        self.image1 = self.image[ 3:image_height-6, 3:image_width-2]
        
        return self.image1

    # check their are only one many people:
    def save_data(self, ID, Fname, Mname, Lname, entry_date):
        
        new_img = image_data[0]
        
        face_locations = face_recognition.face_locations(new_img)

        face_encodings = face_recognition.face_encodings(new_img, face_locations)

        face_names = []
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(faces, face_encoding)
            name = "Not recognize"

            face_distances = face_recognition.face_distance(faces, face_encoding)
            
            
                
            if face_distances.size > 0: # check whether the face_distances is empty or not
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = names[best_match_index]
                    
            else:
                print("Faces list is epty")
            
            face_names.append(name)
        
        i = 0
        for y,w,h,x in face_locations:
            i += 1

        if i == 1:
            # if face_names[i-1] == "Not recognize":
            #     # print("vayo hai")
                
            full_name = Fname + ' ' + Mname + ' ' + Lname
            
            if ID in ids:
                message = f"You enter duplicate ID, {ID} is already in the system."
                self.message = Label(self.info_frame , text = message, fg="red", font=("Helvetica", 12))
                self.message.pack()
                
            else:
                ids.append(ID)
                names.append(full_name)
                faces.append(face_encodings[i-1])
                times.append(entry_date)

                #save jpg image to file folder
                imgName = ID + ".jpg"
                cv2.imwrite( os.path.join(known_dir, imgName), image_data[0])

                #delete old data.
                file = open(os.path.join( known_dir, "faceData.pickle"), 'w')
                file.close()

                #dump new data
                with open(os.path.join( known_dir, "faceData.pickle"), 'wb') as file:
                    pickle.dump([ids, names, faces, times], file)

                self.message = Label(self.info_frame ,text = "Data imported successfully", fg="green", font=("Helvetica", 12))
                self.message.pack()
                
                image_data.remove(image_data[0])
                self.root.destroy()
                # main_for_entry()
                
                
                
            # else:
            #     message = f"Hi {face_names[i-1]}, You already in the system."
            #     self.message = Label(self.info_frame , text = message, fg="blue", font=("Helvetica", 12))
            #     self.message.pack()
            #     image_data.remove(image_data[0])

        elif i == 0:
            message = "No one in the frame !!!!"
            self.message = Label(self.info_frame , text = message, fg="red", font=("Helvetica", 12))
            self.message.pack()
            image_data.remove(image_data[0])
            
        else:
            message = "More than 1 person (or no one) in frame. So, Clear noise."
            self.message = Label(self.info_frame , text = message, fg="red", font=("Helvetica", 12))
            self.message.pack()
            image_data.remove(image_data[0])


def main_for_entry():
    
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
    root.iconbitmap(known_dir+'/logo-icon.ico')
    
    EntryWindow(root, cv2.VideoCapture(1))
    root.mainloop()

if __name__ == "__main__":
        
    main_for_entry()