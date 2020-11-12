import face_recognition
import cv2
import os
import numpy as np
import pickle
print("imported successfully !!!")

known_dir = "C:/Users/Goku/Documents/jupyter_data/known_image"
#load face data from pickle

with open(os.path.join( known_dir, "faceData.pickle"), 'rb') as file:
    names, faces = pickle.load(file)

face_locations = []
face_encodings = []


cap = cv2.VideoCapture(1)

while 1:
    
    _,img = cap.read()
    
    # for front camera:
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.flip(img, 1)

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    face_names = []
    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(faces, face_encoding)
        name = "Not recognize"

        face_distances = face_recognition.face_distance(faces, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = "Hi " + names[best_match_index]

        face_names.append(name)
    i = 0   
    for y,w,h,x in face_locations:

        cv2.rectangle(frame, (x,y), (w,h), (255,0,255), 2)
        cv2.putText(frame, str(face_names[i]), (x, y-5), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0), 2)

        i += 1
    
    
    new_frame = frame # cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow('image',new_frame)

    if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()