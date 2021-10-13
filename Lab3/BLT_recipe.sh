#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_t$

echo "Based on what's in your fridge you can make a BLT!" | festival --tts
echo "Does a BLT sound good?" | festival --tts
#arecord -f cd -r 16000 -d 5 -t wav recorded.wav && sox recorded.wav recorded_m$

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav recorded_mono.wav
python3 BLT_recipe.py recorded_mono.wav
