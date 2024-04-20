import cv2
from detection import AccidentDetectionModel
import numpy as np
import requests

model = AccidentDetectionModel("model.json", 'model_weights.h5')
font = cv2.FONT_HERSHEY_SIMPLEX

def send_alert(probability):
    if probability > 90:
        url = "https://maker.ifttt.com/trigger/accident_alert/json/with/key/YOUR_IFTTT_MAKER_WEBHOOK_KEY"
        data = {"value1": probability}
        requests.post(url, data=data)

def startapplication():
    video = cv2.VideoCapture(2)  # for camera use video = cv2.VideoCapture(0)
    while True:
        ret, frame = video.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (250, 250))

        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
        if (pred == "Accident"):
            prob = (round(prob[0][0] * 100, 2))

            send_alert(prob)

            cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
            cv2.putText(frame, pred + " " + str(prob), (20, 30), font, 1, (255, 255, 0), 2)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    startapplication()
