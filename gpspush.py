# -*- coding: utf-8 -*-

import time
import sys
import serial
import sqlite3

from gps3 import gps3

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

timetmp=""

dbname = 'lora.sqlite3'
conn = sqlite3.connect(dbname,check_same_thread=False)
cur = conn.cursor()

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
