import os
import cv2
import pickle
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,'images')

y_labels = []
x_train = []

current_id = 0
label_ids = {}

for root,dirs,files in os.walk(image_dir):
    for file in files:
        if file.endswith('png'):
            path = os.path.join(root,file)
            label = os.path.basename(root).replace(" ","_").lower()
            #print(path)

            if label not in label_ids:
                label_ids[label]= current_id
                current_id +=1

            id_ = label_ids[label]

            pil_image = Image.open(path)
            image_array = np.array(pil_image,'uint8') # type

            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.2, minNeighbors=5)
            for x,y,w,h in faces:
                roi = image_array[y:y+h,x:x+w]
                x_train.append(roi)
                y_labels.append(id_)

#print(label_ids)

with open('labels.pickle','wb') as f:
    pickle.dump(label_ids,f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainer.yml")
