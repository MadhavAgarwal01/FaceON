import os
import cv2
import time
import numpy as np 
import pickle
from livenessmodel import get_liveness_model
from statistics import mode, StatisticsError
from datetime import date
from datetime import datetime
from csv import DictReader,DictWriter

global present
global ROOT_LOCATION
present = ""

def is_present():

    #==============================================================================================
    
    with open('root.csv','r') as rf:
        csv_reader_root = DictReader(rf,fieldnames = ['ROOT LOCATION'])
        for row in csv_reader_root:
            ROOT_LOCATION = row['ROOT LOCATION']
            os.chdir(ROOT_LOCATION) 

    #==============================================================================================

    #font = cv2.FONT_HERSHEY_SIMPLEX
    font = cv2.FONT_ITALIC 

    #from faces
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

    # check if trainer file is present or not
    try:
        recognizer.read('trainer.yml')
    except cv2.error:
        os.chdir(ROOT_LOCATION)
        return '','FIRST TRAIN FACE DATA !'

    labels = {}
    with open('labels.pickle','rb') as f:
        og_labels = pickle.load(f)
        labels = { v:k for k,v in og_labels.items()}


    # Get the liveness network
    model = get_liveness_model()

    # load weights into new model
    model.load_weights("model/model.h5")
    print("Loaded model from disk")

    # opencv 
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)
    video_capture.set(4, 480)
    count = 0
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Initialize some variables
    input_vid = []
    real_names=[]
    n_str=""

    capture_duration = 10
    start_time = time.time()

    while(int(time.time() - start_time) < capture_duration):
        # Grab a single frame of video
        if len(input_vid) < 24:

            ret, frame = video_capture.read()

            liveimg = cv2.resize(frame, (100,100))
            liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
            input_vid.append(liveimg)
            is_face_present = False
        else:
            ret, frame = video_capture.read()
            
            liveimg = cv2.resize(frame, (100,100))
            liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
            input_vid.append(liveimg)
            inp = np.array([input_vid[-24:]])
            inp = inp/255
            inp = inp.reshape(1,24,100,100,1)
            pred = model.predict(inp)
            input_vid = input_vid[-25:]

            is_face_present = False

            #face_recog
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
            cv2.rectangle(frame, (0,0), (700,45), (0,0,0), cv2.FILLED)

            for x,y,w,h in faces:
                #print(x,y,w,h)
                roi_gray = gray[y:y+h,x:x+w]

                id_,conf = recognizer.predict(roi_gray)

                if conf>=45:# and conf<=85:
                    # Name in live frame
                    name = labels[id_]
                    n_str=name
                    color = (154, 199, 22)
                    color1= ( 255,255,255)
                    stroke = 2
                    cv2.putText(frame,name.upper(),(250,30),font,1,color1,stroke,cv2.LINE_AA)
                    is_face_present = True

                color = (154, 199, 22) #BGR
                stroke = 2
                end_cord_x = (x,y)
                end_cord_y = (x+w,y+h)
                cv2.rectangle(frame,end_cord_x,end_cord_y,color,stroke)

            #cv2.rectangle(frame, (490,0), (590,35), (0,0,0), -1)


            if pred[0][0]> .95:
                cv2.putText(frame,'REAL',(550, 30),font,1,(0,255,0),2,cv2.LINE_AA)
            else:
                if is_face_present:
                    cv2.putText(frame,'FAKE',(550, 30),font,1,(0,0,255),2,cv2.LINE_AA)

            # Display the liveness score in top left corner     
            cv2.putText(frame, str(pred[0][0])[:7], (10, 30), font, 1.0, (255, 255, 0), 2,cv2.LINE_AA)
            # Display the resulting image
            cv2.imshow('Video', frame)


            # PREDICTION 
            if pred[0][0]> .95:
                if count%(1*fps) == 0 and n_str !='':
                    real_names.append(n_str)
                    n_str=""

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    try:
        present = mode(real_names)
        if present=="":
            video_capture.release()
            cv2.destroyAllWindows()
            os.chdir(ROOT_LOCATION)
            return '',"TRY AGAIN!"
            
    except StatisticsError: # when real_names list is empty
        video_capture.release()
        cv2.destroyAllWindows()
        os.chdir(ROOT_LOCATION)
        return '',"TRY AGAIN!"

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    os.chdir(ROOT_LOCATION)
    
    return present,'OK'