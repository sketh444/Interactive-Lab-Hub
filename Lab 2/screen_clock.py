import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import datetime
import qwiic_joystick

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
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

currentDate = datetime.datetime.now()
endDate = datetime.datetime(2029, 7, 22, 9, 45, 0 ) 

#currentDate = time.strftime("%m/%d/%Y %H:%M:%S")
#t = (2029, 7, 22, 9, )
#endDate = time.mktime(t)

timeLeft= endDate - currentDate

yearsLeft = timeLeft.days//360
daysLeft = timeLeft.days%360
minutesLeft = timeLeft.seconds// 60
secondsLeft = timeLeft.seconds % 60
hoursLeft = minutesLeft //60 
minutesLeft = minutesLeft % 60
#endDate_format = datetime.datetime(yearsLeft, daysLeft, hoursLeft, minutesLeft, secondsLeft )

#print(endDate)
#print(currentDate)
#print(timeLeft)

deadline = "0 EMISSIONS DEADLINE" 
help =  "What can you do to help?"
pressButton = "Hold the button to find out"
tips = ["remember to turn off lights","use reusable water bottles", "drive less, bike more", "eat less red meat", "thrift clothing","eat locally grown foods" ]
i = 0
tip = " "
DEADLINE = "DEADLINE"

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

myJoystick = qwiic_joystick.QwiicJoystick()

prev = 512
prev2 = 512 
loop = 0 
screen = False  

#new font 
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",30)

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
	# Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-USD-usage-and-WTTR-load
 
    if not buttonA.value or not buttonB.value:
        tip = tips[i]
        i = (i + 1) % len(tips)

    if myJoystick.connected == True:
        if myJoystick.vertical > 1000 and prev < 1000: #updirection 
            tip = tips[i]
            i = (i + 1) % len(tips)
        if myJoystick.vertical < 100 and prev > 100: #downdirection 
            i = (i - 1) % len(tips)
            if i < 0: 
               i = len(tips) - 1 
            tip = tips[i]
        if myJoystick.horizontal > 1000 and prev2 < 1000:
           screen  = not screen 
        if myJoystick.horizontal < 100 and prev2 > 100:
           screen  = not screen 

    prev = myJoystick.vertical
    prev2 = myJoystick.horizontal

    t = str(yearsLeft) + " " + "years" + " " + str(daysLeft) + " " +  "days" + " " + str(hoursLeft) + ":" + str(minutesLeft) + ":" + str(secondsLeft)    
    # Write four lines of text.
    
    
    if screen == False:
       x, y = 0,0
       draw.text((x, y), deadline, font=font, fill="#FFFFFF")
       y += font.getsize(deadline)[1]
       draw.text((x, y), t, font=font, fill="#FFFFFF")
       y += font.getsize(t)[1]*2
       draw.text((x, y), help, font=font, fill="#FFFFFF")
       y += font.getsize(help)[1]
       draw.text((x, y), pressButton, font=font, fill="#FFFFFF")
       y += font.getsize(pressButton)[1]     
       draw.text((x, y), tip, font=font, fill="#00FF00")
       y += font.getsize(pressButton)[1]
    else:
       if loop % 10 >= 5: 
          draw.text((50, 10), DEADLINE, font=font2, fill="#FF0000")
       else:
          draw.text((50, 10), DEADLINE, font=font2)
       y += font.getsize(DEADLINE)[1]
       draw.text((0, 50), t, font=font, fill="#FFFFFF")
       y += font.getsize(t)[1]*2    

    if loop % 10 == 0:
       delta = datetime.timedelta(seconds=1)
       timeLeft = timeLeft - delta
       yearsLeft = timeLeft.days//360
       daysLeft = timeLeft.days%360
       minutesLeft = timeLeft.seconds// 60 
       secondsLeft = timeLeft.seconds % 60
       hoursLeft = minutesLeft //60 
       minutesLeft = minutesLeft % 60 
#draw.text((x, y), "hshshhshsh", font=font, fill="#FF00FF")
    loop += 1 

    # Display image.
    disp.image(image, rotation)
    time.sleep(.1)
