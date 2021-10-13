#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import json
import string

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), "yes no [unk]")

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
#        print(rec.Result())
#        dumps1 = json.dumps(rec.FinalResult())
#        results1 = json.loads(rec.Result())
        myResult = rec.Result()
        myList = myResult.split("text" )
        s = myList[1]
        print(s)
        s2 = s.split(" : ")
        print(s2)
        print(s2[1])
        s3 = s2[1]
        #print(results1)
        # text1 = results1[1]
       # print(text1)
        if len(s3) > 2:
           print("ahahahhah")
           os.popen('sh /home/pi/Interactive-Lab-Hub/Lab3/test.sh')
#    else:
 #       print(rec.PartialResult())

print(rec.FinalResult())
print(data)
results1 = json.loads(rec.FinalResult())
print(results1)
#text1 = results1[1]
#print(text1)
