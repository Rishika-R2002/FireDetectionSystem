import cv2
import numpy as np
import winsound
import smtplib
import threading
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

Fire_reported = 0
Alarm_Status = False
Email_Status = False
def play_audio():
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def send_mail_function():

    recipientEmail = "fire department mail"
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("ucs19326@rmd.ac.in", "24-Apr-2002")
        server.sendmail("ucs19326@rmd.ac.in", "sabarivasan64443@gmail.com", "Warning A Fire Accident has been reported on ABC Company")
        print("sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
       print(e)

video = cv2.VideoCapture(0)
while True:
    ret, frame = video.read()
    frame = cv2.resize(frame, (1000,600))
    blur = cv2.GaussianBlur(frame, (15,15), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]

    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')

    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame, hsv, mask=mask)

    size = cv2.countNonZero(mask)

    if int(size) > 15000:
        Fire_reported = Fire_reported + 1

        if Fire_reported >= 1:
            if Alarm_Status == False:
                play_audio()
                Alarm_Status = True
            if Email_Status == False:
                talk('warning!')
                talk('A fire spark detected in section 13')
                talk('An email is sent to the fire department')
                threading.Thread(target=send_mail_function).start()
                Email_Status = True


    if ret == False:
        break
    cv2.imshow("Cam", output)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyWindow()
video.release()

