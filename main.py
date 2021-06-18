import cv2
import numpy as np
import winsound
import smtplib
import threading
import pyttsx3
import ibm_db
import datetime
date,time = str(datetime.datetime.now()).split();
time = time.strip(".")
originaltime,garbagge=time.split(".")
conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=khn40929;PWD=rlt63tx5m+1v6mts;", "", "")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

Fire_reported = 0
Alarm_Status = False
Email_Status = False
def play_audio():
    stmt = ibm_db.exec_immediate(conn,"INSERT INTO details (time,date,place) VALUES('{}','{}','{}');".format(originaltime,date,"NULL"))

    num = ibm_db.num_rows(stmt)

    winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def send_mail_function():

    recipientEmail = "ucs19324@rmd.ac.in"
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("rishikarishi1402@gmail.com", 'Richu@1402')
        server.sendmail('rishikarishi1402@gmail.com', recipientEmail, "Warning A Fire Accident has been reported on ABC Company")
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
