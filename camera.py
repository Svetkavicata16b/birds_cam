import os
from datetime import datetime
from gpiozero import LED, MotionSensor
from time import sleep
from picamera2 import Picamera2, Preview
import ftplib


# define host, username, password and port
HOSTNAME = "78.130.244.248"
USERNAME = "ivo"
PASSWORD = "***"
PORT = 21

# define pins
LED_PIN = 2
MOTION_SENSOR_PIN = 5

# init
led = LED(LED_PIN)
sleep(5)
led.off()
motion = MotionSensor(MOTION_SENSOR_PIN)
picam2 = Picamera2()
picam2.start_preview(Preview.NULL)


# this is function which determines file’s name  relative to time
def get_name():
    name = "img_"
    out_format = "%Y%m%d_%H%M%S"
    dtime = datetime.now()
    suff = dtime.strftime(out_format)
    name += suff
    return name


# capture bird’s image
def get_img(name):
    picam2.start_and_capture_file(name)


# send image to ftp
def send_to_ftp(name, hostname, username, password, port):
    ftp_server = ftplib.FTP()
    ftp_server.connect(hostname, port)
    ftp_server.login(username, password)
    ftp_server.cwd("/ivo/imgs")
    
    with open(name, "rb") as file:
        ftp_server.storbinary("STOR {}".format(name), file)
    
    ftp_server.quit()


# main function – call other functions to build main loop
def main():
    while True:
        motion.wait_for_motion()
        name = get_name()
        file_path = "%s.jpg" % name
        
        led.on()
        sleep(1)
        led.off()
        
        get_img(file_path)
        send_to_ftp(file_path, HOSTNAME, USERNAME, PASSWORD, PORT)
        os.remove(file_path)
    
        sleep(10)


# call main function
if __name__ == "__main__":
    main()