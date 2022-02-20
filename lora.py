# -*- coding: utf-8 -*-

# ソフトシリアル経由でLoRaモジュールを読む

import serial
import RPi.GPIO as GPIO
import struct
import time
import sys

#ResetPin = 26
#ResetPin = 12


def printable(l):
    x = struct.unpack(str(len(l)) + 'b', l)
    y = ''
    for i in x:
        if i >= 0 and i!=13 and i!=10:
            y = y + chr(i)
    return y

class LoRa():
    def __init__(self, rpin, sport):
        self.resetPin = rpin
        self.port = sport
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.resetPin, GPIO.OUT)
        GPIO.output(self.resetPin, 1)

        #self.s = serial.Serial('/dev/ttyS0', 115200)
        self.s = serial.Serial(self.port, 115200)#, timeout=0.5)
        #self.s = serial.Serial('/dev/ttyAMA1', 115200)

    def reset(self):
        GPIO.output(self.resetPin, 0)
        time.sleep(0.1)
        GPIO.output(self.resetPin, 1)

    def open(self):
        self.s.open()

    def close(self):
        self.s.close()

    def readline(self, timeout = None):
        if timeout != None:
            self.s.close()
            self.s.timeout = timeout
            self.s.open()
        line = self.s.readline()
        if timeout != None:
            self.s.close()
            self.s.timeout = None
            self.s.open()
        return line

    def write(self, msg):
        self.s.write(msg.encode('utf-8'))

    def parse(self, line):
        fmt = '4s4s4s' + str(len(line) - 14) + 'sxx'
        data = struct.unpack(fmt, line)
        hex2i = lambda x: int(x, 16) if int(x, 16) <= 0x7fff else ~ (0xffff - int(x, 16)) + 1
        rssi = hex2i(data[0])
        panid = hex2i(data[1])
        srcid = hex2i(data[2])
        msg = data[3].decode('utf-8')
        return (rssi, panid, srcid, msg)

    def send(self, msg=""):
        ret = 0
        time.sleep(0.01)
        msg_fin = '\r\n'
        msg=str(msg)+msg_fin
        self.write(msg)
        self.s.flush()
        while (True):
            line = self.readline()
            print(line)
            if 'OK' in printable(line):
                ret = 1
                print('msg sent successfully')
                break
            elif 'NG' in printable(line):
                ret = 0
                print(msg)
                print('msg sent failed')
                break

        sys.stdout.flush()
        return ret
    
    def recieve(self):
        while (True):
            line = self.readline()
            if len(line) >= 14:
                break
        data = self.parse(line)

        rssi = data[0]
        pan = data[1]
        sd = data[2]
        msg = data[3]

        sys.stdout.flush()
        return rssi,pan,sd,msg

def main():
    lr = LoRa()
    while True:
        data = lr.parse(lr.readline())
        print(data)

if __name__ == "__main__":
    main()
