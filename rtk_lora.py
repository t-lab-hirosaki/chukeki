# -*- coding: utf-8 -*-

import time
import sys
import threading
import sqlite3
import datetime
import serial

from gps3 import gps3

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

import set_lora
import r_profile as rp
import lora

dbname = 'lora.sqlite3'

lr1 = lora.LoRa(12, '/dev/serial0')
p_data1=rp.read('lora_profile1')

#受信
sl1 = set_lora.set_LoRa(lr1,p_data1)

def recieve_main():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    while True:
        try:
            rssi,pan,sd,msg = lr1.recieve()
            print("data recieved",rssi,pan,sd,msg)
            sql = 'INSERT INTO lora_data(ch,sf,rssi,panid,dstid,data) VALUES(' + str(p_data1['channel']) + ',' + str(p_data1['sf']) + ',' + str(rssi) + ',' + str(pan) + ',' + str(sd) + ',"' + msg + '");'
            cur.execute(sql)
            conn.commit()

        except Exception as e:
            print("connection failed")
            print(e)
            conn.close()
            break
    conn.close()

def gps_rec():
    conn = sqlite3.connect(dbname,check_same_thread=False)
    cur = conn.cursor()
    timetmp=""

    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if data_stream.TPV['time'] != timetmp:
                print('time : ', data_stream.TPV['time'])
                print('lat : ', data_stream.TPV['lat'])
                print('lon : ', data_stream.TPV['lon'])
                print("")
                if data_stream.TPV['time'] != "n/a":
                    try:
                        sql = 'INSERT INTO gps_data(lat,lng,date) VALUES(' + str(data_stream.TPV['lat']) + ',' + str(data_stream.TPV['lon']) + ',"' + str(data_stream.TPV['time']) + '");'
                        cur.execute(sql)
                        conn.commit()
                    except Exception as e:
                        print("connection failed")
                        print(e)
                        conn.close()
                        break
            timetmp = data_stream.TPV['time']
            time.sleep(0.1)
        
    conn.close()

if __name__ == "__main__":
    print("start")
    
    while True:
        print("a")
        if sl1.setMode():
            break
    
    """
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    sql = 'DELETE FROM gps_data;'
    cur.execute(sql)
    conn.commit()
    conn.close()
    time.sleep(1)
    """

    #thread1 = threading.Thread(target=recieve_main,daemon=True)
    #thread1.start()

    while True:
        gps_rec()
        time.sleep(10)
    
