import board
import busio
import adafruit_apds9960.apds9960
import time
import paho.mqtt.client as mqtt
import uuid
import signal
from vosk import Model, KaldiRecognizer
import subprocess
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from subprocess import Popen, call



# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


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

height =  disp.height
width = disp.width 
image = Image.new("RGB", (height, width))
draw = ImageDraw.Draw(image)

rotation = 90

font = ImageFont.truetype("usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)


import os
import json
import wave

def record():
    os.system('arecord -D hw:2,0 -f cd -c1 -r 48000 -d 4 -t wav recorded_input.wav')
    f = wave.open('recorded_input.wav', 'rb')
    model = Model('model')
    rec = KaldiRecognizer(model, f.getframerate())
    while True:
        data = f.readframes(4000)
        if len(data)==0:
            break
        rec.AcceptWaveform(data)
    i = json.loads(rec.FinalResult())['text']
    print('You said: ', i)
    return i

def speak(val):
    subprocess.run(["sh", "speak.sh", val])

topic = 'IDD/walkietalkie'

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)

def on_message(cleint, userdata, msg):
    # if a message is recieved on the colors topic, parse it and set the color
    if msg.topic == topic:
        text = msg.payload.decode('UTF-8')
        speak(text)
        draw.rectangle((0, 0, height, width), fill=(0,0,0))
        draw.text((0,0), text, font=font)
        disp.image(image, rotation)
        time.sleep(0.01)
    print(text)

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect
client.on_message = on_message

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

#client.loop_forever()

# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)

# hen sigint happens, do the handler callback function
signal.signal(signal.SIGINT, handler)

while True:
    print('Recording')
    msg = record()
    print('Done recording', msg)
    if len(msg)>0:
        client.publish(topic, msg)
    time.sleep(3)

    break

client.loop_forever()
