# -*- coding: utf-8 -*-

import ast
import time
import struct
import sys
import serial


import r_profile as rp
import lora

class set_LoRa():
    def __init__(self, lr, p_data):
        self.lr = lr
        self.p_data = p_data

    def printable(self, l):
        x = struct.unpack(str(len(l)) + 'b', l)
        y = ''
        for i in x:
            if i >= 0 and i!=13 and i!=10:
                y = y + chr(i)
        return y

    def sendcmd(self, cmd):
        self.lr.write(cmd)
        t = time.time()
        print(cmd)
        while (True):
            if (time.time() - t) > 5:
                print('panic: %s' % cmd)
                exit()
            line = self.lr.readline()
            print(self.printable(line))
            if 'OK' in self.printable(line):
                return True
            elif 'NG' in self.printable(line):
                return False

    def setMode(self):
        self.lr.s.reset_input_buffer()
        self.lr.reset()
        time.sleep(2.0)
        self.lr.write('config\r\n')
        time.sleep(0.1)
        self.lr.reset()
        while True:
            time.sleep(1)
            line = self.lr.readline()
            print(line)
            if 'Mode' in self.printable(line):
                self.lr.s.reset_input_buffer()
                time.sleep(3)
                line = self.sendcmd('2\r\n')
                print(line)
                if not line:
                    print("return")
                    return False
                break

        line = self.sendcmd('a %d\r\n' % self.p_data['node'])
        if not line:
            print("return node")
            return False
        time.sleep(0.2)
        line = self.sendcmd('bw %d\r\n' % self.p_data['bw'])
        if not line:
            print("return bw")
            return False
        time.sleep(0.2)
        line = self.sendcmd('sf %d\r\n' % self.p_data['sf'])
        if not line:
            print("return sf")
            return False
        time.sleep(0.2)
        line = self.sendcmd('d %d\r\n' % self.p_data['channel'])
        if not line:
            print("return channel")
            return False
        
        time.sleep(0.2)
        self.sendcmd('e %s\r\n' % str(self.p_data['panid']))
        time.sleep(0.2)
        self.sendcmd('f %s\r\n' % str(self.p_data['ownid']))
        time.sleep(0.2)
        self.sendcmd('g %s\r\n' % str(self.p_data['dstid']))
        time.sleep(0.2)
        self.sendcmd('l 1\r\n')
        time.sleep(0.2)
        self.sendcmd('m 1\r\n')
        time.sleep(0.2)
        self.sendcmd('p 1\r\n')
        time.sleep(0.2)
        self.sendcmd('o 1\r\n')
        time.sleep(0.2)
        self.sendcmd('q 2\r\n')
        time.sleep(0.2)
        self.sendcmd('w\r\n')
        self.lr.reset()
        print('LoRa module set to new mode')
        sys.stdout.flush()

        return True