#from socket import *
import socket
import collections
from collections import deque
import re
import subprocess
import time

class MessageSplitter(object):
    def __init__(self, settings, maxlen=10):
        self.buffer = collections.deque(maxlen=maxlen)
        self.deviceName = settings.deviceName
        
    def Split(self, msg):
        regex = str(self.deviceName) + r"(.*)"
        msgBody = re.findall(regex, msg)[0]
        regex = "MSGID(\d+)"
        msgID = re.findall(regex, msg)[0]
        if msgID in self.buffer:
            return (False, "message already recieved", -1)
        self.buffer.append(msgID)
        return (True, msgBody, msgID)

class Settings(object):
    def __init__(self, port=12345, timeout=60, deviceName="PIREMOTE"):
        self.port = port
        self.timeout = timeout
        self.deviceName = deviceName

def GetCommandBlocking(settings):
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(settings.timeout)
        s.bind(('',settings.port))
        m=s.recvfrom(1024)
        valid = True
        return (valid, m[0])
    except socket.timeout as msg:
        valid = False
        return (valid, "timeout")
    except Exception as msg:
        import time
        time.sleep(1)
        valid = False
        msg = msg.message + " " + msg.strerror
        return (valid, msg)

def RunRemote(settings):
    subprocess.call("/home/pi/Desktop/start_lirc.sh")
    splitter = MessageSplitter(settings)
    while True:
        try:
            (valid, msg) = GetCommandBlocking(settings)
            print "recieved UDP text: " + msg
            if not valid:
                continue
    
            (valid, msgBody, msgID) = splitter.Split(msg)
            if not valid:
                print(msgBody)
                continue
    
            # now we process the command and do what it says
            if "turn on" or "turn off" in msgBody:
                subprocess.call("/home/pi/Desktop/turn_on.sh")
            else:
                print("I dont recognize this command:")            
                print "ID: " + msgID
                print "Body: " + msgBody
        except Exception as exp:
                print exp
                time.sleep(1)
                


if __name__ == "__main__":
    settings = Settings()
    RunRemote(settings)
