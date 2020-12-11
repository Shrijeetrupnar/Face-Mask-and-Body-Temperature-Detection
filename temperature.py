from smbus2 import SMBus
from mlx90614 import MLX90614
import RPi.GPIO as GPIO
import time
import os
import lcd
from time import sleep
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer=23 
GPIO.setup(buzzer,GPIO.OUT)


GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
bus=SMBus(1)
sensor = MLX90614(bus, address=0x5A)
f = open("mask.txt","r")
mon= f.read()
print "Ambient Temperature :", sensor.get_ambient()
print "Body Temperature :", sensor.get_object_1()
capture_temperature= sensor.get_object_1()

if sensor.get_object_1() < 37 and mon != '0':
    GPIO.setwarnings(False)
    GPIO.output(17, True)
    lcd.lcd_init()
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Please Proceed...",2)
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(3)
    GPIO.output(17, False)
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Opening Door.",2)
    lcd.GPIO.cleanup()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(13,GPIO.OUT)
    servo1 = GPIO.PWM(13,50)
    servo1.start(0)
    time.sleep(2)
    duty = 2
    servo1.ChangeDutyCycle(7)
    time.sleep(10)
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    servo1.stop()
    GPIO.cleanup()

else:
    GPIO.setwarnings(False)
    GPIO.output(18, True)
    lcd.lcd_init()
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("STOP!!!",2)
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(1)
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(1)
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(3)
    GPIO.output(18, False)
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Door will not open",2)
    lcd.GPIO.cleanup()
    fromaddr = "sender's email address"
    toaddr = "Receiver's email address "

    # instance of MIMEMultipart
    msg = MIMEMultipart()
     
    # storing the senders email address
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "ALERT!!!..."
     
    # string to store the body of the mail
    body = MIMEText('''
    <html>
        <body>
            <h1>Alert!!</h1>
            <h2>Person has entered the premises without mask or high temperature.. </h2>
            <p>Temp: '''+str(capture_temperature)+'''</p>
            <h2>Time: {}</h2>
        </body>
    </html>'''.format(datetime.datetime.now()), 'html', 'utf-8')
     
    # attach the body with the msg instance
    msg.attach(body)
     
    # open the file to be sent
    filename = "image.jpg"
    attachment = open("image.jpg", "rb")
     
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
     
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "sender's email password")
    # Converts the Multipart msg into a string
    text = msg.as_string() 
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
     
    s.quit()
bus.close()
