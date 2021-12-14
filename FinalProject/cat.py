import board
import busio
#import adafruit_apds9960.apds9960
import time
import paho.mqtt.client as mqtt
import uuid
import signal
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import qwiic_button
from omxplayer.player import OMXPlayer
import adafruit_mpr121
from adafruit_servokit import ServoKit
#initalize green button
my_button = qwiic_button.QwiicButton()
my_button.LED_off()
# Initialize the board and touch sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)
#==============servo==============
# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)
# Name and set up the servo according to the channel you are using.
servo1 = kit.servo[0]
servo2 = kit.servo[15]
# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
#If the servo didn't sweep the full expected range, then try adjusting the minimum and maximum pulse widths
#using set_pulse_width_range(min_pulse, max_pulse).
servo1.set_pulse_width_range(500, 2500)
servo2.set_pulse_width_range(500, 2500)
#==============MQTT==============
#topic for sending and reciveing messages
topic = 'IDD/cat'
#files
file_purr = 'purr.wav'
file_meow = 'meow.mp3'
def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)
def on_message(cleint, userdata, msg):
    # if a message is recieved on the colors topic, parse it and set the color
    if msg.topic == topic:
        text = msg.payload.decode('UTF-8')
        print(text)
        if text == 'Zoogy' and mycat == True:
            my_button.LED_on(150)
            time.sleep(5)
            my_button.LED_off()
        # if text == 'back_top':
        #     OMXPlayer(file_meow)
client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect
client.on_message = on_message
client.connect(
    'farlab.infosci.cornell.edu', port=8883)
# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)
# hen sigint happens, do the handler callback function
signal.signal(signal.SIGINT, handler)
# assigning body parts of the cat to be touched to the touch sensor
catbody = {0:'paw', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5'}
client.loop_start()
mycat = False
while True:
    for i in range(12):
        if mpr121[i].value:
            mycat = True
            val = f'{catbody[i]}'
            print(val)
            catname = 'Ransom'
            client.publish(topic, catname)
            if val == '0':
                OMXPlayer(file_purr)
                time.sleep(2)
            if val == '1':
                OMXPlayer(file_meow)
                time.sleep(2)
            if val == '0':
                servo1.angle = 45
                time.sleep(1)
                servo1.angle = 10
            if val == '2':
                servo2.angle = 30
                time.sleep(1)
                servo2.angle = 10
            time.sleep(1)
