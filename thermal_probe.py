#!/usr/bin/python3
import os, glob, time
from time import time as looptime
from time import sleep
from datetime import datetime

# add the lines below to /etc/modules (reboot to take effect)
# w1-gpio
# w1-therm

class DS18B20(object):
    def __init__(self):        
        self.device_file = glob.glob("/sys/bus/w1/devices/28*")[0] + "/w1_slave"
        
    def read_temp_raw(self):
        f = open(self.device_file, "r")
        lines = f.readlines()
        f.close()
        return lines
        
    def crc_check(self, lines):
        return lines[0].strip()[-3:] == "YES"
        
    def read_temp(self):
        temp_c = -255
        attempts = 0
        
        lines = self.read_temp_raw()
        success = self.crc_check(lines)
        
        while not success and attempts < 3:
            time.sleep(.2)
            lines = self.read_temp_raw()            
            success = self.crc_check(lines)
            attempts += 1
        
        if success:
            temp_line = lines[1]
            equal_pos = temp_line.find("t=")            
            if equal_pos != -1:
                temp_string = temp_line[equal_pos+2:]
                temp_c = float(temp_string)/1000.0
        
        return temp_c

if __name__ == "__main__":

    while True:
        sleep(60 - looptime() % 60)
###---Everything inside here has to be run in the loop---###
        obj = DS18B20()

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        dirout = os.getcwd()+"/data/"
        fileout = "blah.txt"

        if not os.path.exists(dirout):
            os.mkdir(dirout)
    
        if not os.path.isfile(dirout+fileout):
            fileout = open(dirout+fileout,"w")
            print("#Date(dd/mm/yyyy) Time(hh:mm:ss) Temperature(C)",file=fileout)
        else:
            fileout = open(dirout+fileout,"a")
        print(dt_string, obj.read_temp())
        print(dt_string, obj.read_temp(), file=fileout)
        fileout.close()
###---------------------------------------------------------###
#   print(os.path.isfile(dirout+fileout))
#    exit()
#    fileout = open("blah.txt","a")
#    print("Temp: %s C" % obj.read_temp())
