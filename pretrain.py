import cv2
import numpy as np
import os
from PIL import Image

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

Face_ID = -1 
pev_person_name = ""
y_ID = []
x_train = []

face_dataset = os.path.join(os.getcwd(), "dataset")

for root, dirs, files in os.walk(face_dataset):
    if dirs == []:
        print("Dataset for {}:".format(os.path.basename(root)))
    for i, file in enumerate(files):
        if file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png"): 
            path = os.path.join(root, file)
            person_name = os.path.basename(root)
            print("[INFO] processing image {}/{}".format(i + 1, len(files)))


            if pev_person_name != person_name:
                Face_ID = Face_ID + 1 
                pev_person_name = person_name


            Gery_Image = Image.open(path).convert("L")
            Crop_Image = Gery_Image.resize( (800,800) , Image.ANTIALIAS)
            Final_Image = np.array(Crop_Image, "uint8")
            faces = face_cascade.detectMultiScale(Final_Image, scaleFactor=1.05, minNeighbors=6, minSize=(30, 30)) 
            print(Face_ID,faces)

            for (x,y,w,h) in faces:
                roi = Final_Image[y:y+h, x:x+w]
                x_train.append(roi)
                y_ID.append(Face_ID)
                # break

recognizer.train(x_train, np.array(y_ID))
recognizer.save("pre-trained.yml")
