#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Are you ready for the final step?" | festival --tts

#arecord -f cd -r 16000 -d 5 -t wav recorded.wav && sox recorded.wav recorded_m$

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav recorded_mono.wav
python3 BLT_recipe4.py recorded_mono.wav
