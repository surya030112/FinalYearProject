import cv2
from detection import AccidentDetectionModel
import numpy as np
import os
import serial
import time

# Replace with the port your NodeMCU is connected to
port = 'COM9'

# Set the baud rate
baudrate = 9600

# Open the serial connection
ser = serial.Serial(port, baudrate)

model = AccidentDetectionModel("model.json", 'model_weights.h5')
font = cv2.FONT_HERSHEY_SIMPLEX

def startapplication():
    video = cv2.VideoCapture("sample.mp4")
    while True:
        ret, frame = video.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (250, 250))

        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
        if(pred == "Accident"):
            prob = (round(prob[0][0]*100, 2))
            
            # to beep when alert:
            if(prob > 70):
                  ser.write(b'y')

    # Wait for 5 seconds
                # time.sleep(5)
            #     os.system("say beep")
             # Send the character 'y' to the NodeMCU
          

            cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
            cv2.putText(frame, pred+" "+str(prob), (20, 30), font, 1, (255, 255, 0), 2)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            return
        cv2.imshow('Video', frame)  


if __name__ == '__main__':
    startapplication()