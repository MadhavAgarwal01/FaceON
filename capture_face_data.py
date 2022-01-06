import cv2
import os
import numpy as np
from csv import DictReader,DictWriter

global ROOT_LOCATION

def capture_biometrics(name_og):

    #==============================================================================================

    with open('root.csv','r') as rf:
        csv_reader_root = DictReader(rf,fieldnames = ['ROOT LOCATION'])
        for row in csv_reader_root:
            ROOT_LOCATION = row['ROOT LOCATION']
            os.chdir(ROOT_LOCATION) 

    #==============================================================================================

    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    cap = cv2.VideoCapture(0)

    name = name_og.replace(' ',"_")

    # ==============images directory=====================
    if os.path.exists('images'):
        pass
    else:
        os.mkdir('images')

    # images
    p = os.getcwd()
    pi = os.path.join(p,'images')
    os.chdir(pi)

    # images folder exists or not
    if os.path.exists(name):
        pass
    else:
        os.mkdir(name)

    p_name = os.path.join(pi,name)
    os.chdir(p_name)

    num=1
    while(True):
        ret, frame = cap.read()
        #frame = cv2.flip(frame,0) # flips vertically
        #frame = cv2.flip(frame,1) # flips horizontally
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for x,y,w,h in faces:
            roi_gray = gray[y:y+h,x:x+w]

            color = (255,50,50) #BGR
            stroke = 2
            end_cord_x = (x,y)
            end_cord_y = (x+w,y+h)
            cv2.rectangle(frame,end_cord_x,end_cord_y,color,stroke)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,str(num),(5,25),font, 1,(255,255,255),2,cv2.LINE_AA)
            cv2.imshow('Frame',frame)
            
            img_item = str(num) +'.png'
            cv2.imwrite(img_item,roi_gray)
            
        num =num+1
        if cv2.waitKey(100) == ord('q'):
            break
        elif num>=100:
            break

    cap.release()
    cv2.destroyAllWindows()

    os.chdir(ROOT_LOCATION) 
    return "FACE DATA CAPTURED SUCCESSFULLY !"