import face_recognition
import cv2
import os
import numpy as np
import pickle

known_dir = "C:/Users/Goku/Documents/jupyter_data/known_image"

try:
    #load face data from pickle
    with open(os.path.join( known_dir, "faceData.pickle"), 'rb') as file:
        names, faces = pickle.load(file)


    print("Available attendee names: ")
    for name in names:
        print(name)


    newnames = []
    newfaces = []

    print("Enter the name to remove attendence data.< quit to cancel >")
    print("'All' to Erase everything.")

    del_name = input(">>: ")



    if del_name == 'quit':

        print("Data removing process has been cancelled !!")
        # fgdsgsdsdg

    elif del_name == 'All' or del_name == 'all':

        delete_conformation = input("Are you sure to Erase everything ?(yes/no)")

        if delete_conformation == 'yes':
            #Erase everything from the data base
            file = open(os.path.join( known_dir, "faceData.pickle"), 'w')
            file.close()

            print("All data removed successfully.")

        else:
            print("Data removing process has been cancelled !!")


    else:
        if del_name in names: # name available or not in list
            conf = input("Are you want to delete {}'s data.(yes/no) : ".format(del_name))
            if conf == 'yes':
                for name, face in zip(names, faces):  # zib both lists together
                    if name != del_name:             # append all name as it is except deleted name's data
                        newnames.append(name)
                        newfaces.append(face)
                #delete old data.
                file = open(os.path.join( known_dir, "faceData.pickle"), 'w')
                file.close()
            
                #dump new data
                with open(os.path.join( known_dir, "faceData.pickle"), 'wb') as file:
                    pickle.dump([newnames, newfaces], file)
                
                #delete .jpg file also from known_dir
                image_name = del_name + ".jpg"
                del_path = os.path.join(known_dir, image_name)
                os.remove(del_path)
                print(f"{del_name}'s data removed successfully.")

            else:      # if conf == 'no'
                print("Data removing process has been cancelled !!")

        else:       # if name isnot in the list.
            print("Name is not in the list.!!")


except Exception as e:
    print("Your Database is Empty!!!")
    print("Please Enter data to remove it.")