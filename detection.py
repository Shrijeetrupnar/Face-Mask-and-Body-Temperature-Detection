import os
from time import time
import tensorflow as tf
from tensorflow.keras.models import save_model, Sequential

model_path = "model2-009.model"
model = tf.keras.models.load_model(model_path)
save_model(model,model_path + r"model-010.h5", save_format='h5')

import cv2
import numpy as np
from keras.models import load_model
model=load_model("./model2-009.modelmodel-010.h5")

labels_dict={0:'without mask',1:'mask'}
color_dict={0:(0,0,255),1:(0,255,0)}

size = 4
webcam = cv2.VideoCapture(0)
prev = time()
delta = 0

classifier = cv2.CascadeClassifier('/home/mayur/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')

while True:
    (rval, im) = webcam.read()
    im=cv2.flip(im,1,1) 
    
    current = time()
    delta += current - prev
    prev = current

    mini = cv2.resize(im, (im.shape[1] // size, im.shape[0] // size)) 
    faces = classifier.detectMultiScale(mini)
    # Draw rectangles around each face
    for f in faces:
        (x, y, w, h) = [v * size for v in f]
        face_img = im[y:y+h, x:x+w]
        resized=cv2.resize(face_img,(150,150))
        normalized=resized/255.0
        reshaped=np.reshape(normalized,(1,150,150,3))
        reshaped = np.vstack([reshaped])
        result=model.predict(reshaped)
        # print(result)
        
        current = time()
        delta += current - prev
        prev = current
        ret, frame = webcam.read()
        if delta > 5:
                cv2.imwrite("./image.jpg",frame)
                delta = 0
        label=np.argmax(result,axis=1)[0]
        if label == 1 :
            print("Mask Detected...\n")
            with open('mask.txt','w+') as f:
                f.write("1")
            # resultlist.append("Mask Detected")
        else:
            print("...Mask NOT Detected...\n")
            with open('mask.txt','w+') as f:
                f.write('0')
            # resultlist.append("Mask Not Detected")
        cv2.rectangle(im,(x,y),(x+w,y+h),color_dict[label],2)
        cv2.rectangle(im,(x,y-40),(x+w,y),color_dict[label],-1)
        cv2.putText(im, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
    
    # Show the image
    cv2.imshow('LIVE',   im)
    key = cv2.waitKey(10)

    # Esc to break out of the loop 
    if key == 27:
        break
webcam.release()
cv2.destroyAllWindows()