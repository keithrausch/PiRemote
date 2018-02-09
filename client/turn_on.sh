#!/bin/bash
sudo lircd --device /dev/lirc0
irsend SEND_ONCE Vizio KEY_POWER
echo "sent turn on command"