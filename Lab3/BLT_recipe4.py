#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import time

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
                os.popen('sh /home/pi/Interactive-Lab-Hub/Lab3/step4.sh') 
                time.sleep(20) 
                break
            else:
                os.popen('sh /home/pi/Interactive-Lab-Hub/Lab3/notready.sh')
                time.sleep(25)
                os.popen('sh /home/pi/Interactive-Lab-Hub/Lab3/step4.sh')     
                break 
