import os
import time

while True:
    os.system("scp mask.txt pi@192.168.1.65:/home/pi/iot")
    os.system("scp image.jpg pi@192.168.1.65:/home/pi/iot")
    time.sleep(2)