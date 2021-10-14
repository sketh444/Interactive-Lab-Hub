import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import board
import busio
#from adafruit_apds9960.apds9960 import APDS9960
import time
import sys
import digitalio
import os
from vosk import Model, KaldiRecognizer
import wave
import json
import shlex
from subprocess import Popen, call

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
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

def speak(val):
    subprocess.run(["sh", "GoogleTTS_demo.sh", val])


def check_userinput():
    os.system("arecord -D hw:2,0 -f cd -c1 -r 48000 -d 4 -t wav recorded_mono.wav")
    wf = wave.open("recorded_mono.wav", "rb")

    model = Model("model")
    # rec = KaldiRecognizer(model, wf.getframerate())
    rec = KaldiRecognizer(model, wf.getframerate(), "yes no")
    #'["black","beige","blue","brown","green","grey","navy","orange","red","yellow","yes","start"," [unk]"]')

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    reply = json.loads(rec.FinalResult())
    print("User's reply: ", reply["text"])
    return reply["text"]

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 23)
smartFridge = "I am a smart fridge !"
draw.rectangle((0, 0, width, height), outline=0, fill=0)
draw.text((0, 50), smartFridge, font=font, fill="#FFFFFF")
disp.image(image, rotation)
time.sleep(2)

while True: 
    image = Image.open("IDD_step1.jpg")
    image = image.convert("RGB")
    image = image.resize((width, height), Image.BICUBIC)
    disp.image(image, rotation)
    speak("Based on what's in your fridge you can make a BLT! Does a BlT sound good?")
    reply_BLT = check_userinput()
    if len(reply_BLT) == 3: 
        image = Image.open("IDD_step2.jpg")
        image = image.convert("RGB")
        image = image.resize((width, height), Image.BICUBIC)
        disp.image(image, rotation)
        speak("Great lets get started! Step 1: take out bread, lettace, tomato, bacon, and mayo from your fridge")
    else: 
        speak("It appears that you need to go grocery shopping or order take out tonight")
        break
    time.sleep(10)
    speak("Are you ready for the next step ?")
    reply_ready = check_userinput()
    if len(reply_ready) == 3:
        image = Image.open("IDD_step3.jpg")
        image = image.convert("RGB")
        image = image.resize((width, height), Image.BICUBIC)
        disp.image(image, rotation)
        speak("Turn on stove, place a pan on the stove, place bacon in the pan, cook until brown")
    else: 
       speak("No worries, I will give you 20 seconds to catch up before telling you the next step")
       time.sleep(10)
       image = Image.open("IDD_step3.jpg")
       image = image.convert("RGB")
       image = image.resize((width, height), Image.BICUBIC)
       disp.image(image, rotation)
       speak("Turn on stove, place a pan on the stove, place bacon in the pan cook until brown") 
    time.sleep(10)
    speak("Are you ready for the next step ?")
    reply = check_userinput()
    if len(reply) == 3:
       image = Image.open("IDD_step4.jpg")
       image = image.convert("RGB")
       image = image.resize((width, height), Image.BICUBIC)
       disp.image(image, rotation)
       speak("Chop lettace and tomato")
    else:  
       speak("No worries, I will give you 20 seconds to catch up before telling the next step ")
       time.sleep(10)
       image = Image.open("IDD_step4.jpg")
       image = image.convert("RGB")
       image = image.resize((width, height), Image.BICUBIC)
       disp.image(image, rotation)
       speak("Chop lettace and tomato")
    time.sleep(10)
    speak("Are you ready for the final step ?")
    reply = check_userinput()
    if len(reply) == 3:
       image = Image.open("IDD_step5.jpg")
       image = image.convert("RGB")
       image = image.resize((width, height), Image.BICUBIC)
       disp.image(image, rotation)
       speak("Spread mayo on bread, place chopped lettace, tomato, and cook bacon in the bread")
       speak("Enjoy your BLT!")
    else: 
       speak("No worries, I will give you 20 seconds to catch up before telling the next step ")
       time.sleep(10)
       image = Image.open("IDD_step5.jpg")
       image = image.convert("RGB")
       image = image.resize((width, height), Image.BICUBIC)
       disp.image(image, rotation)       
       speak("Spread mayo on bread, place chopped lettace, tomato, and cook bacon in the bread")
       speak("Enjoy your BLT!")   
    break 
