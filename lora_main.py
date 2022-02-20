# -*- coding: utf-8 -*-

import time
import sys
import subprocess
import threading
import sqlite3
import datetime

import set_lora
import r_profile as rp
import lora

dbname = 'lora.sqlite3'

lr1 = lora.LoRa(12, '/dev/serial0')
lr2 = lora.LoRa(26, '/dev/ttyAMA1')
p_data1=rp.read('lora_profile1')
p_data2=rp.read('lora_profile2')

#受信
sl1 = set_lora.set_LoRa(lr1,p_data1)
#送信
sl2 = set_lora.set_LoRa(lr2,p_data2)

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
            print("connection failed2")
            print(e)
            conn.close()
            break
    conn.close()

def send_main():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    while True:
        try:
            now = datetime.datetime.today()
            now = now - datetime.timedelta(minutes=5) 
            sql = 'SELECT * FROM lora_data where datetime > "' + str(now) + '" order by id asc limit 1'
            cur.execute(sql)
            dbdata = cur.fetchall()
            if dbdata:
                print("send_data",dbdata)
                dbtime = str(dbdata[0][7])[14:16] + str(dbdata[0][7])[17:19]
                msgres = lr2.send(str(dbdata[0][6]) + ":" + str(hex(dbdata[0][5])[2:]) + ":" + dbtime)

                if msgres:
                    sql = 'DELETE FROM lora_data where id = ' + str(dbdata[0][0]) 
                    cur.execute(sql)
                    conn.commit()

        except Exception as e:
            print("connection failed1")
            print(e)
            conn.close()
            break

        time.sleep(1)
    conn.close()

if __name__ == "__main__":
    print("start")
    
    while True:
        if sl1.setMode():
            break
    while True:
        if sl2.setMode():
            break

    lr1.s.reset_input_buffer()
    lr2.s.reset_input_buffer()
    
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    now = datetime.datetime.today()
    now = now - datetime.timedelta(minutes=5) 
    sql = 'SELECT * FROM lora_data where datetime < "' + str(now) + '" order by id desc limit 1'
    cur.execute(sql)
    dbdata = cur.fetchall()
    print(dbdata)
    if dbdata:
        print("delete",str(dbdata[0][0]))
        sql = 'DELETE FROM lora_data WHERE id <= "' + str(dbdata[0][0]) + '"'
        cur.execute(sql)
        conn.commit()
    

    cmd = 'vcgencmd measure_temp'
    tmp = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).stdout.readlines()
    tmp = tmp[0].decode('utf-8')[5:]
    print(tmp)
    
    sql = 'INSERT INTO lora_data(ch,sf,rssi,panid,dstid,data) VALUES(0,0,0,0,0,"s' + tmp + '");'
    cur.execute(sql)
    conn.commit()
    conn.close()
    time.sleep(1)
    thread1 = threading.Thread(target=recieve_main,daemon=True)
    thread1.start()

    while True:
        try:
            send_main()
            time.sleep(10)
        except:
            print("Exception")
    
