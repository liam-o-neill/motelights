#!/usr/bin/env python

from sys import exit
from random import randint

try:
    import paho.mqtt.client as mqtt
except ImportError:
    exit("This example requires the paho-mqtt module\nInstall with: sudo pip install paho-mqtt")
import time
from colorsys import hsv_to_rgb
import motephat as mote

old_command="b'on'"
command="b'on'"
MQTT_SERVER = "192.168.1.31"
MQTT_PORT = 1883
MQTT_TOPIC = "PiforLiam/motephat"

# Set these to use authorisation
MQTT_USER = None
MQTT_PASS = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global old_command
    global command
    command=str(msg.payload)
    print("message: " + str(msg.payload) +  "," + command)
    if command == "off":
	command = "b'off'"
    if command == "on":
	command = "b'on'"
    if command == "b'off'":
        old_command = "b'off'"
        print("turn off")
        return
    if command == "b'RAINBOW'":
        old_command = "b'RAINBOW'"
        print("RAINBOW")
        return
    if command == "b'on'":
        old_command = "b'on'"
        print("turn on")
        return
    if command[2:5] == "RGB":
        old_command = command
        print("RGB")
        return
    if command[2:8] == "BRIGHT":
        print("BRIGHT")
        return
    if command == "b'KITT'":
        old_command = "b'KITT'"
        print("KITT")
        return
    if command[2:8] == "RANDOM":
        old_command = command
        print("Random")
        return
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)
mote.set_brightness(0.2)
#mote.clear()
#mote.show()
client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message

if MQTT_USER is not None and MQTT_PASS is not None:
    print("Using username: {un} and password: {pw}".format(un=MQTT_USER, pw="*" * len(MQTT_PASS)))
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)
client.connect(MQTT_SERVER, MQTT_PORT, 60)
client.loop_start()
kittChannel=0
kittLight=0
while True:
    if command == "b'on'":
#        print(" were on")
        h = time.time() * 5
        for channel in range(4):
           for pixel in range(16):
               hue = (h + 68) % 360
               r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
               mote.set_pixel(channel + 1, pixel, r, g, b)
    if command == "b'RAINBOW'":
#        print(" were rainbow")
        h = time.time() * 50
        for channel in range(4):
           for pixel in range(16):
               hue = (h + (channel * 64) + (pixel * 4)) % 360
               r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
               mote.set_pixel(channel + 1, pixel, r, g, b)
    if command == "b'off'":
#        print(" were off")
        mote.clear()
    if command[2:5] == "RGB":
#        print(" were rgb")
        r = command[6:9]
        g = command[10:13]
        b = command[14:17]
        for channel in range(4):
            for pixel in range(16):
#                 time.sleep(0.01)
                mote.set_pixel(channel + 1, pixel, r, g, b)
            time.sleep(0.01)
    if command[2:8] == "BRIGHT":
#        print(" were bright")
        bright = float(command[9:12]) 
        mote.set_brightness(bright)
        command = old_command
    if command == "b'KITT'":
#        print(" were kitt")
        if kittChannel==2:
           if kittLight==16:
               k=-1
        if kittChannel==0:
           if kittLight==0:
               k=1
        kittLight=kittLight+k
        if kittLight>16:
           kittChannel=kittChannel+k
           kittLight=0
        if kittLight < 0:
           kittChannel=kittChannel+k
           kittLight=16
        for channel in range(3):
            for pixel in range(16):
                if channel==kittChannel:
                    if pixel==kittLight:
#                       time.sleep(0.01)
                       mote.set_pixel(channel + 1, pixel, 255, 0, 0)
                    if pixel != kittLight:
#                       time.sleep(0.01)  
                       mote.set_pixel(channel + 1, pixel, 0,0,0)               
                else:
#                     time.sleep(0.01) 
                     mote.set_pixel(channel + 1, pixel, 0, 0, 0)
            time.sleep(0.01)
    if command[2:8] == "RANDOM":
#        print(" were random")
        t=float(command[9:12])
        r=randint(0,48)
        g=randint(0,48)
        b=randint(0,48)
        cr = r//16
        cg = g//16
        cb = b//16
        pr = r%16
        pg = g%16
        pb = b%16
        for channel in range(4):
            for pixel in range(16):
                r=0
                g=0
                b=0
                if channel==cr:
                   if pixel==pr:
                      r=255
                if channel==cg:
                   if pixel==pg:
                      g=255
                if channel==cb:
                   if pixel==pb:
                      b=255
                mote.set_pixel(channel + 1, pixel, r, g, b)
            time.sleep(t)
    mote.show()
    





