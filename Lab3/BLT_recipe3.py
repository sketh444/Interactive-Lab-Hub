#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

# Display the image
disp.image(image, rotation)

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)
model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), "yes no")

while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data): 
            myResult = rec.Result()
            myList = myResult.split("text" )
            s = myList[1]
            s2 = s.split(" : ")
            s3 = s2[1]
            print(s3)
            print(len(s3))
            if len(s3) == 7:
                image = Image.open("IDD_step4.jpg")
                image = image.convert("RGB")
                image = image.resize((width, height), Image.BICUBIC)
                disp.image(image, rotation)
                os.popen('sh /home/pi/Interactive-Lab-Hub/Lab3/step3.sh') 
                time.sleep(20)
                os.popen('sh /home/pi/Interactive-Lab-Hub/Lab3/next3.sh') 
                break
            else:
                image = Image.open("IDD_step3.jpg")
                image = image.convert("RGB")
                image = image.resize((width, height), Image.BICUBIC)
                disp.image(image, rotation)
                os.popen('sh /home/pi/Interactive-Lab-Hub/Lab3/notready.sh')
                time.sleep(25)
                image = Image.open("IDD_step4.jpg")
                image = image.convert("RGB")
                image = image.resize((width, height), Image.BICUBIC)
                disp.image(image, rotation)
                os.popen('sh /home/pi/Interactive-Lab-Hub/Lab3/step3.sh')     
                break  
