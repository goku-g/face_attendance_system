import face_recognition
import cv2
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
import time

known_dir = "C:/Users/Goku/Documents/jupyter_data/known_image"
exit = False # variable for exit.

#load face data from pickle

with open(os.path.join( known_dir, "faceData.pickle"), 'rb') as file:
    names, faces = pickle.load(file)

face_locations = []
face_encodings = []

print("  ")

cap = cv2.VideoCapture(1)

# data entry function:
def enterName(photo, imageData):
    
    print("You are new to the system.")    
    naam = input("Enter your name here.<for cancellation type q >  Name: ")
    if naam == 'q':
        print("cancelled !!!")
    else:
        imgName = naam + ".jpg"
        cv2.imwrite( os.path.join(known_dir, imgName), photo)
        names.append(naam)
        faces.append(imageData)
        
        #delete old data.
        file = open(os.path.join( known_dir, "faceData.pickle"), 'w')
        file.close()
        
        #dump new data
        with open(os.path.join( known_dir, "faceData.pickle"), 'wb') as file:
            pickle.dump([names, faces], file)
        print("Your name is save as {}.".format(naam))

        #cv2.imshow("saved image", cv2.cvtColor(photo, cv2.COLOR_BGR2RGB))
       
def imrotate(im2rotate):
	im2rotate = cv2.rotate(im2rotate, cv2.ROTATE_90_COUNTERCLOCKWISE)
	im2rotate = cv2.flip(im2rotate, 1)
	return im2rotate

# check their are only one many people:
def check_whois():
    global exit
    
    _,new_img = cap.read()
    
    # for front camera of phone using droid cam:
    new_img = imrotate(new_img)
    
    face_locations = face_recognition.face_locations(new_img)
    
    face_encodings = face_recognition.face_encodings(new_img, face_locations)
    
    face_names = []
    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(faces, face_encoding)
        name = "Not recognize"

        face_distances = face_recognition.face_distance(faces, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = names[best_match_index]

        face_names.append(name)
        
    i = 0
    for y,w,h,x in face_locations:
        i += 1

    if i == 1:
        if face_names[i-1] == "Not recognize":
            # cv2.destroyWindow('image')
            enterName(new_img, face_encodings[i-1])
        else:
            print("Hi {}, You already in the system.".format(face_names[i-1]))
            
    elif i > 1:
        print("More than 1 person in frame. So, Clear noise.")

    else:
        print("You are not in the frame.")
        
    exit = True


# detect mouse event:
def mouse_click(event, click_x, click_y,flags, param): 
    global exit
    
    # to check if left mouse  
    # button was clicked 
    if event == cv2.EVENT_LBUTTONDOWN: 
        pos = [click_x, click_y]
        # was clicked.
        #   print(pos)
        if click_x > img_x-165 and click_y > img_y-40 and click_x < img_x and click_y < img_y:
            check_whois()
        #   0,img_y-40),(120,img_y
        if click_x > 0 and click_y > img_y-40 and click_x < 120 and click_y < img_y:
            print("cancelled !!!")
            exit = True



while 1:

    _,img = cap.read()
    
    #exit = True

    # for front camera of phone using droid cam:
    img = imrotate(img)

    (img_y,img_x,l) = img.shape

    img = cv2.rectangle(img, (img_x-165,img_y-40),(img_x-2,img_y-2),(255,255,255),-1)
    cv2.putText(img,'Save Data',(img_x-163,img_y-10),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,0),2)

    img = cv2.rectangle(img, (0,img_y-40),(120,img_y),(255,255,255),-1)
    cv2.putText(img,'Cancel',(5,img_y-10),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,0),2)

    frame = img

    cv2.setMouseCallback('image', mouse_click)
    
    cv2.imshow('image',img)
    
    # exit from external functions.
    if exit:
        #print("working...")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


print("  ")
cap.release()
cv2.destroyAllWindows()