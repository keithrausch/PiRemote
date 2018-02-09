#!/bin/sh

sleep 10
touch /home/pi/Desktop/FileCreatedByBootScript.txt
python /home/pi/Desktop/RecieveCommand.py &
