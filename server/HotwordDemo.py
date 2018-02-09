#!/usr/bin/env python3

import logging
logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
logging.disable(logging.CRITICAL)
logging.debug('started script')

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import miaHotword
import random
import os.path

logging.debug('finished most imports')

from UDPRemote import *

def main():
    logging.debug('checking internet connection')
    
    import urllib
    from urllib.request import urlopen, Request
    while True:
        try:
            url = "https://www.google.com"
            urlopen(url)
            status = "Connected"
            break
        except:
            status = "Not connected"
            print(status)
    
    logging.debug('internet connected')
    # do stuff...
    
    
    logging.debug('started main')
    aiy.voicehat.get_status_ui().status('starting')
    logging.debug('about to start cloud speed recognizer')
    try:
        recognizer = aiy.cloudspeech.get_recognizer()
    except Exception as e:
        logging.debug(e.__doc__)
        logging.debug(e.message)
    logging.debug('started cloud speed recognizer')
    recognizer.expect_phrase('turn on')
    recognizer.expect_phrase('turn off')
    
    logging.debug('about to get led')
    led = aiy.voicehat.get_led()
    recorder=aiy.audio.get_recorder()    
    recorder.start()
    voice_only=False
    seconds=0

    udpRemote = UDPRemote()
    logging.debug('about to speak')
    aiy.audio.say('Starting')
    logging.debug('spoke')
         
    while True:
        miaHot=miaHotword.miaHotword()
        aiy.voicehat.get_status_ui().status('ready')
        miaHot.waitForHotword(recorder,voice_only,1)

        aiy.voicehat.get_status_ui().status('listening')
        text = recognizer.recognize()
        aiy.voicehat.get_status_ui().status('thinking')
        if not text:
            aiy.voicehat.get_status_ui().status('error')
            #aiy.audio.say('Sorry?')
        else:
            print('You said "', text, '"')
            if 'turn on' in text or 'turn off' in text:
                udpRemote.Send(text)
                aiy.audio.say('ok')

    aiy.voicehat.get_status_ui().status('stopping')
    aiy.voicehat.get_status_ui().status('power-off')              
if __name__ == '__main__':
    main()
    # To run the demo say the hotword and then ask about a holiday
