#!/bin/sh 
sleep 10
touch /home/pi/Desktop/FILETOUCHEDATBOOT.txt
cd /home/pi/AIY-voice-kit-python/src
/home/pi/AIY-voice-kit-python/env/bin/python3 /home/pi/AIY-voice-kit-python/src/HotwordDemo.py &