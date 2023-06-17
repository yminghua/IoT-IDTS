import cv2 
import numpy as np
import os
from PIL import Image
from send_email import *
import time
from servo import *

# sudo pigpiod

face_dataset = os.path.join(os.getcwd(), "dataset")
labels = [dir for dir in os.listdir(face_dataset)]
print("Known users:", labels)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("pre-trained.yml")

cap = cv2.VideoCapture(cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

pan = Servo(pin=12, max_angle=90, min_angle=-90)
tilt = Servo(pin=13, max_angle=30, min_angle=-30)
panAngle = 0
tiltAngle = 0
pan.set_angle(panAngle)
tilt.set_angle(tiltAngle)

time.sleep(1)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("./warnings/record_"+time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())+".mp4", fourcc, 10, (640, 480))

unknownCount = 0
start_time = time.time()
previous_time = start_time

sweep_step = 1
frame_number = 0

def patrol(panAngle, tiltAngle, sweep_step):
    if panAngle >= 90 or panAngle <= -90:
        sweep_step = -sweep_step
    panAngle += sweep_step
    pan.set_angle(panAngle)
    if tiltAngle != 0:
        tiltAngle += int(-tiltAngle/abs(tiltAngle))*0.5
        tilt.set_angle(tiltAngle)
    return panAngle, tiltAngle, sweep_step

while(True):

    _, img = cap.read()
    frame_number += 1
    img = cv2.flip(img, 0)
    # img = cv2.flip(img, 1)
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30))
    isKnown = True
    patrol_mode = True
    track_x, track_y, track_w, track_h = 0, 0, 0, 0
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]

        id_, distance = recognizer.predict(roi_gray)
        #print(id_, distance)

        font = cv2.FONT_HERSHEY_SIMPLEX
        if distance <= 70:
            name = labels[id_]
            cv2.putText(img, name, (x,y-10), font, 1, (255,0,0), 2)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        else:
            isKnown = False    
            cv2.putText(img, "Unknown", (x,y-10), font, 1, (0,0,255), 2)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            track_x, track_y, track_w, track_h = x, y, w, h

    cv2.imshow('Preview',img)
    
    if not isKnown:
        unknownCount += 1
        if unknownCount >= 5:
            patrol_mode = False
            pan_update, tilt_update = calculate_angle(x+w/2, y+h/2)
            panAngle += pan_update
            panAngle = check_pan_angle(panAngle)
            tiltAngle += tilt_update
            tiltAngle = check_tilt_angle(tiltAngle)
            pan.set_angle(panAngle)
            tilt.set_angle(tiltAngle)
        if unknownCount >= 10:
            out.write(img)
            #print("===Find Somebody Unknown===")
            current_time = time.time()
            if current_time - previous_time >= 600 or previous_time == start_time:  # 10 mins
                previous_time = current_time
                file_name = "./warnings/" + time.strftime("%y-%m-%d_%H-%M-%S", time.localtime()) + ".jpg"
                cv2.imwrite(file_name, img)
                response = email_warning(file_name)
                #if response.status_code == 200:
                    #print("Warning email is already sent")
    else:
        unknownCount = 0
        
    if frame_number % 2 == 0:
        if patrol_mode:
            panAngle, tiltAngle, sweep_step = patrol(panAngle, tiltAngle, sweep_step)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
